#!/bin/bash
#trans json to BIOE
python json2BIO.py -i ./AGAC_training -o ./outtrain
#separate train data and test data
for i in `ls ./outtrain |head -75`;
do
mv ./outtrain/$i ./outtrain-0.3
done
for i in `ls ./outtrain |head -175`;
do
mv ./outtrain/$i ./outtrain-0.7
done
echo 'separate down!'
echo '#####################'
############run wapiti
#train
wapiti train -a sgd-l1 -t 3 -i 10 -p ./Tok321.pat <(cat ./outtrain-0.7/*.tab) ./agac_train.mod
#dump
wapiti dump ./agac_train.mod ./agac_train.txt
#label
wapiti label -c -m ./agac_train.mod <(cat ./outtrain-0.3/*.tab) ./agac_test.tab
#conlleval.pl
perl /public/home/zcyu/ref/NLP/2019SpringTextM/conlleval.pl -d $'\t' < ./agac_test.tab | tee ./agac_test.eval

