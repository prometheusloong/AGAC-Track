# AGAC-Track task 1

This repository is a practice for AGAC Track. The AGAC Task is part of the BioNLP Open Shared Tasks (BioNLP-OST: http://2019.bionlp-ost.org) and meets the BioNLP-OST standard of quality, originality and data formats. The track has three tasks(task comment is following), and the repository challenges task 1 until now. We used two methods to come true Named-entity recognition. One of methods is wapiti which a software based on CRF. And another method is BLSTM-CNN-CRF which based on nerual network. In fact the BLSTM-CNN-CRF is better than wapiti.
- Task 1: Trigger words NER
    Recognize the trigger words in PubMed abstracts and annotated them as correct trigger labels or entities (Var, MPA, Interaction, Pathway, CPA, Reg, PosReg, NegReg, Disease, Gene, Protein, Enzyme). 
- Task 2: Themetic roles identification
    Identify the themetic roles (ThemeOf, CauseOf) between trigger words. 
- Task 3: "Gene;Function change;disease" link discovery
    Extract the gene-function change-disease link. For example , "Mutations in SHP-2 phosphatase that cause hyperactivation of its catalytic activity have been identified in human leukemias, particularly juvenile myelomonocytic leukemia.", from this sentence, the participants need to extract SHP-2;GOF;juvenile myelomonocytic leukemia.

Detailed information could visit AGAC Track website:
- https://sites.google.com/view/bionlp-ost19-agac-track/home (main site),
- http://120.79.44.74:8000/BioNLP_OST_AGAC (image site).

## Environment Requirements
#### wapiti
- python 3
- spacy
- wapiti (best add to environment)

#### BLSTM-CNN-CRF
- python 3.6
- tensorflow 1.12

You could use conda to configure the environment easily.
```    conda create --name agac_task1 python=3.6 
    conda init
    conda activate agac_task1
    conda install tensorflow-gpu=1.12 (or conda install tensorflow=1.12 if you dont have a gpu)
```    

## Usage
### data format
```
Mutations NNPS B-Var
in IN O
SHP-2 NNP B-Gene
phosphatase NN B-Enzyme
that WDT O
cause VBP O
hyperactivation NN B-PosReg
of IN O
```

/wapiti/json2BIO.py could transform .json file to BIO format
```
cd wapiti/
python json2BIO.py -i ../data -o ./outtrain
-i input .json file
-o output BIO file
```

And you should splite the BIO data to 7:3 (train data and test data for wapiti) and 6:2:2 (train data, test data and dev data for blstm-cnn-crf), randomly.

### wapiti
```
#train
wapiti train -a sgd-l1 -t 3 -i 10 -p ./pat/Tok321.pat <(cat ./outtrain-0.7/*.tab) ./agac_train.mod
#dump
wapiti dump ./agac_train.mod ./agac_train.txt
#label
wapiti label -c -m ./agac_train.mod <(cat ./outtrain-0.3/*.tab) ./agac_test.tab
#evaluation
perl /public/home/zcyu/ref/NLP/2019SpringTextM/conlleval.pl -d $'\t' < ./agac_test.tab | tee ./agac_test.eval
```
You could change the parameter and pat file to adjust the result, detail information could see the wapiti manual:
- https://wapiti.limsi.fr/manual.html

### BLSTM-CNN-CRF
You should put 3 files(train.txt, test.txt and dev.txt) at blstm-cnn-crf/data/agac_nospecial/

The parameter: 
```
######################################################
#
# Data preprocessing
#
######################################################
datasets = {
    'agac_nospecial':                                   #Name of the dataset
        {'columns': {0:'tokens', 1:'POS', 2:'chunk_BIO'},   #CoNLL format for the input data. Column 0 contains tokens, column 2 contains POS and column 2 contains chunk information using BIO encoding
         'label': 'chunk_BIO',                                #Which column we like to predict
         'evaluate': True,                                  #Should we evaluate on this task? Set true always for single task setups
         'commentSymbol': None}                             #Lines in the input data starting with this string will be skipped. Can be used to skip comments
}

# :: Path on your computer to the word embeddings. Embeddings by Komninos et al. will be downloaded automatically ::
embeddingsPath = 'komninos_english_embeddings.gz'
```
And run:
```
python Train_Chunking.py
```

## Results (On test data)
### wapiti
```
processed 14257 tokens with 1071 phrases; found: 508 phrases; correct: 197.
accuracy:  86.67%; precision:  38.78%; recall:  18.39%; FB1:  24.95
              CPA: precision:  15.00%; recall:   6.00%; FB1:   8.57  40
          Disease: precision:  21.15%; recall:  14.86%; FB1:  17.46  52
           Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
             Gene: precision:  44.19%; recall:  12.58%; FB1:  19.59  43
      Interaction: precision: 100.00%; recall:  18.18%; FB1:  30.77  2
              MPA: precision:  12.50%; recall:   3.60%; FB1:   5.59  40
           NegReg: precision:  55.81%; recall:  40.68%; FB1:  47.06  86
          Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  2
           PosReg: precision:  41.98%; recall:  25.76%; FB1:  31.92  81
          Protein: precision:  66.67%; recall:   5.56%; FB1:  10.26  3
              Reg: precision:  25.00%; recall:   6.35%; FB1:  10.13  16
              Var: precision:  46.48%; recall:  29.60%; FB1:  36.16  142
```
### BLSTM-CNN-CRF
```
Scores from epoch with best dev-scores:
  Dev-Score: 0.3284
  Test-Score 0.3927
```

## Acknowledgment
A note about Neural network for NER.
- https://www.paperweekly.site/papers/notes/146

The method used the BLSTM-CNN-CRF from UKPLab. Thank you for contributing this to the community.
- https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf.git



