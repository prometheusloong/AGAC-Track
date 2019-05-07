#!/bin/bash

# Test training and test of wapiti on TAC ADR data
# For documentation on wapiti, see wapiti --help
# and https://wapiti.limsi.fr/

BINDIR=$(dirname $0)

#================
# option processing

input_dir="outtrain"
output_dir="./bio"
pattern_file="./Tok321.pat"
training_options=' -a sgd-l1 -t 3 -i 10 '
debug=0
verbose=0

while getopts i:o:p:r:t:dvh OPTION
do
    case ${OPTION} in
        i) input_dir=${OPTARG};;
        o) output_dir=${OPTARG};;
        p) pattern_file=${OPTARG};;
        t) training_options=${OPTARG};;
	d) debug=1;;
	v) verbose=1;;
      \?|h) echo "Usage: $0 [ -dvh ] [ -i input_dir ] [ -t training_options ]

Train CRF on training part of the corpus.
Apply CRF model on test part of the corpus.
Evaluate the results.

 -i input_dir	Name of input directory containing the corpus (must be in *.tab files starting with uppercase letter).
 -o output_dir	Name of output directory, in which result files are created.
 -p pattern_file	Name of pattern file that specifies features for the CRF (wapiti).  Must end with '.pat'.
 -t training_options	Training options for the CRF (wapiti). Protect with quotes because it contains spaces.

-h	show this message
" 1>&2
	    exit 2;;
    esac
done

# pass the options
shift $((${OPTIND} - 1))
#================

echo "================ Processing from $input_dir to $output_dir ================" 1>&2
if [ ! -d $input_dir ]; then
    echo "Input directory '$input_dir' does not exist" 1>&2
    exit 1
fi

if [ ! -f $pattern_file ]; then
    echo "Pattern file '$pattern_file' does not exist" 1>&2
    exit 2
fi

patname=$(basename $pattern_file .pat)
corpus_name=$(basename $input_dir)

mkdir -p $output_dir		# create if does not exist

echo "input_dir=$input_dir
output_dir=$output_dir
pattern_file='$pattern_file'
training_options='$training_options'
" 1>&2



echo "================ Training $corpus_name (this may take some time) ================" 1>&2
# training: create a MODEL based on PATTERNS and TRAINING-CORPUS
# wapiti train -p PATTERNS TRAINING-CORPUS MODEL
echo "wapiti train $training_options -p $pattern_file <(cat $input_dir/[A-S]*.tab) $output_dir/$patname-train-$corpus_name.mod" 1>&2
wapiti train $training_options -p $pattern_file <(cat $input_dir/[A-S]*.tab) $output_dir/$patname-train-$corpus_name.mod
# wapiti train -a bcd -t 2 -i 5 -p t.pat train-bio.tab t-train-bio.mod
#
# Note: The default algorithm, l-bfgs, stops early and does not succeed in annotating any token (all O)
# sgd-l1 works; bcd works

# To examine the contents of the model, first dump it into a text file then use 'less FILE' to view its contents
wapiti dump $output_dir/$patname-train-$corpus_name.mod $output_dir/$patname-train-$corpus_name.txt

echo "================ Inference $corpus_name ================" 1>&2
# inference (labeling): apply the MODEL to label the TEST-CORPUS, put results in TEST-RESULTS
# wapiti label -m MODEL TEST-CORPUS TEST-RESULTS
# -c : check (= evaluate)
# <(COMMAND ARGUMENTS ...) : runs COMMAND on ARGUMENTS ... and provides the results as if in a file
echo "wapiti label -c -m $output_dir/$patname-train-$corpus_name.mod <(cat $input_dir/[T-Z]*.tab) $output_dir/$patname-train-test-$corpus_name.tab" 1>&2
wapiti label -c -m $output_dir/$patname-train-$corpus_name.mod <(cat $input_dir/[T-Z]*.tab) $output_dir/$patname-train-test-$corpus_name.tab
# wapiti label -c -m t-train-bio.mod test-bio.tab t-train-test-bio.tab

echo "================ Evaluation with conlleval.pl $corpus_name ================" 1>&2
# evaluate the resulting entities
# $'\t' is a way to obtain a tabulation in bash
echo "sudo $BINDIR/conlleval.pl -d $'\t' <$output_dir/$patname-train-test-$corpus_name.tab | tee $output_dir/$patname-train-test-$corpus_name.eval" 1>&2
perl $BINDIR/conlleval.pl -d $'\t' <$output_dir/$patname-train-test-$corpus_name.tab | tee $output_dir/$patname-train-test-$corpus_name.eval
