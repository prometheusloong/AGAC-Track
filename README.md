# AGAC-Track task 1

This repository is a practice for AGAC Track. The AGAC Task is part of the BioNLP Open Shared Tasks (BioNLP-OST: http://2019.bionlp-ost.org) and meets the BioNLP-OST standard of quality, originality and data formats. The track has three tasks(task content is following), and the repository challenges task 1 until now. We used two methods to come true Named-entity recognition. One of methods is wapiti which a software based on CRF. And another method is BLSTM-CNN-CRF which based on nerual network. In fact the BLSTM-CNN-CRF is better than wapiti.
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
- wapiti (best add to environment variable)

#### bidirectional LSTM
- python 3.6
- tensorflow 1.12

#### BLSTM-CNN-CRF
- python 3.6
- tensorflow 1.12

You could use conda to configure the environment easily.
``` 
    conda create --name agac_task1 python=3.6 
    conda init
    conda activate agac_task1
    conda install tensorflow-gpu=1.12 cudatoolkit=9.0(or conda install tensorflow=1.12 if you dont have a gpu.You can also choose the version of cudatoolkit according to your CUDA's version.)
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

/wapiti/json2BIO.py could transform .json file to BIO format. 
It will delete special charater(like β and so on) and print to screen.
```
cd wapiti/
python json2BIO.py -i ../data -o ./outtrain
-i input .json file.
-o output BIO file.
-s choose delete special character(like β) or not, F is delete.
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

### bidirectional LSTM
You should divide your dataset into three files (train.txt, test.txt and dev.txt). Put them into the neural network.For pretrain, download [word2vec](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit)

Run with:
```
python experiment.py config.conf
```
#### Configuration
- path_train - Path to the training data, in CoNLL tab-separated format. One word per line, first column is the word, last column is the label. Empty lines between sentences.
- path_dev - Path to the development data, used for choosing the best epoch.
- path_test - Path to the test file. Can contain multiple files, colon separated.
- conll_eval - Whether the standard CoNLL NER evaluation should be run.
- main_label - The output label for which precision/recall/F-measure are calculated. Does not affect accuracy or measures from the CoNLL eval.
- model_selector - What is measured on the dev set for model selection: "dev_conll_f:high" for NER and chunking, "dev_acc:high" for POS-tagging, "dev_f05:high" for error detection.
- preload_vectors - Path to the pretrained word embeddings, in word2vec plain text format. If your embeddings are in binary, you can use convertvec to convert them to plain text.
- word_embedding_size - Size of the word embeddings used in the model.
- crf_on_top - If True, use a CRF as the output layer. If False, use softmax instead.
- emb_initial_zero - Whether word embeddings should have zero initialisation by default.
- train_embeddings - Whether word embeddings should be updated during training.
- char_embedding_size - Size of the character embeddings.
- word_recurrent_size - Size of the word-level LSTM hidden layers.
- char_recurrent_size - Size of the char-level LSTM hidden layers.
- hidden_layer_size - Size of the extra hidden layer on top of the bi-LSTM.
- char_hidden_layer_size - Size of the extra hidden layer on top of the character-based component.
- lowercase - Whether words should be lowercased when mapping to word embeddings.
- replace_digits - Whether all digits should be replaced by 0.
- min_word_freq - Minimal frequency of words to be included in the vocabulary. Others will be considered OOV.
- singletons_prob - The probability of mapping words that appear only once to OOV instead during training.
- allowed_word_length - Maximum allowed word length, clipping the rest. Can be necessary if the text contains unreasonably long tokens, eg URLs.
- max_train_sent_length - Discard sentences longer than this limit when training.
- vocab_include_devtest - Load words from dev and test sets also into the vocabulary. If they don't appear in the training set, they will have the default representations from the preloaded embeddings.
- vocab_only_embedded - Whether the vocabulary should contain only words in the pretrained embedding set.
- initializer - The method used to initialize weight matrices in the network.
- opt_strategy - The method used for weight updates.
- learningrate - Learning rate.
- clip - Clip the gradient to a range.
- batch_equal_size - Create batches of sentences with equal length.
- epochs - Maximum number of epochs to run.
- stop_if_no_improvement_for_epochs - Training will be stopped if there has been no improvement for n epochs.
- learningrate_decay - If performance hasn't improved for 3 epochs, multiply the learning rate with this value.
- dropout_input - The probability for applying dropout to the word representations. 0.0 means no dropout.
- dropout_word_lstm - The probability for applying dropout to the LSTM outputs.
- tf_per_process_gpu_memory_fraction - The fraction of GPU memory that the process can use.
- tf_allow_growth - Whether the GPU memory usage can grow dynamically.
- main_cost - Control the weight of the main labeling objective.
- lmcost_max_vocab_size = Maximum vocabulary size for the language modeling loss. The remaining words are mapped to a single entry.
- lmcost_hidden_layer_size = Hidden layer size for the language modeling loss.
- lmcost_gamma - Weight for the language modeling loss.
- char_integration_method - How character information is integrated. Options are: "none" (not integrated), "concat" (concatenated), - "attention" (the method proposed in Rei et al. (2016)).
- save - Path to save the model.
- load - Path to load the model.
- garbage_collection - Whether garbage collection is explicitly called. Makes things slower but can operate with bigger models.
- lstm_use_peepholes - Whether to use the LSTM implementation with peepholes.
- random_seed - Random seed for initialisation and data shuffling. This can affect results, so for robust conclusions I recommend running multiple experiments with different seeds and averaging the metrics.
### BLSTM-CNN-CRF
You should put 3 files(train.txt, test.txt and dev.txt) at blstm-cnn-crf/data/agac_nospecial/

The parameter: 
```
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
F1-Score:
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



