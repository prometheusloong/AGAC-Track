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
- wapiti

#### BLSTM-CNN-CRF
- python 3.6
- tensorflow 1.12
  You could use conda to configure the environment easily.
```    conda create --name agac_task1 python=3.6 
    conda init
    conda activate agac_task1
    conda install tensorflow-gpu=1.12 (or conda install tensorflow=1.12 if you havent a gpu)
```    

## Usage
