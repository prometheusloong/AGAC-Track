# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 21:56:14 2019

@author: Pro
"""
import os
import re
import json
import sys, getopt
try:
   opts,args=getopt.getopt(sys.argv[1:],"hi:o:")
except getopt.GetoptError:
   sys.exit(2)
for option,value in opts:
   if option in ('-h'):
       sys.exit()
   elif option in ('-i'):
       infile=value
   elif option in ('-o'):
       outputfile=value

def mkdir(path): # mkdir ouputfile
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
#import nltk
#nltk.data.path.append(r'/public/home/zcyu/ref/NLP/nltk_data')
#token = nltk.word_tokenize(text)
#token = TreebankWordTokenizer().tokenize(text)
#span_generator = TreebankWordTokenizer().span_tokenize(text)
#spans = [span for span in span_generator]

#import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

#######################################
def json_load(address):#json file load
    trainfile = []
    for info in os.listdir(address):
        domain = os.path.abspath(address)
        info1 = os.path.join(domain,info)
        with open(info1) as f:
            data = json.load(f)
        trainfile.append(data)
        f.close()
    return trainfile

def split_word(txt):
    #spacy split word
    tokens = []
    spans = []
    doc = nlp(txt)
    for token in doc:
        tokens.append(token.text)
        spans.append(token.idx)
    #'-' combine
    #spans '-' combine
    lineindex = []
    for g in range(len(tokens)):
        if tokens[g] == '-':
            lineindex.append(g)
            lineindex.append(g + 1)
    for ix in sorted(lineindex, reverse=True):
        del spans[ix]
    #tokens '-' combine
    co = tokens.count('-')
    for c in range(co):
        tokenslink = []
        for i in range(len(tokens)):
            if tokens[i] == '-':
                tlink = tokens[i-1] + '-' + tokens[i+1]
                tokenslink.append(tlink)
                break
            elif tokens[i+1] != '-':
                tokenslink.append(tokens[i])
        for j in range(len(tokens)-i-2):
            tokenslink.append(tokens[j+i+2])
        tokens = tokenslink
    return spans,tokens

def trans_formal(sps,toks,denote):
    index = 0
    label = []
    out = []
    outblank = []
    #label is info from json. like:['p53', 'Gene', 183, 186]
    for i in range(len(denote)):
        label.append([text[denote[i]['span']['begin']:denote[i]['span']['end']], denote[i]['obj'], 
                      denote[i]['span']['begin'], denote[i]['span']['end']])
    #transform to BIO
    for i in range(len(label)):
        cizu = re.split(r' ', label[i][0])
        while index < len(toks):
            if len(cizu) == 1:
                if sps[index] == label[i][2]:
                    out.append([toks[index], 'B-' + label[i][1]])
                    index += 1
                    break
                else:
                    out.append([toks[index], 'O'])
                    index += 1
            else:
                if sps[index] == label[i][2]:
                    out.append([toks[index], 'B-' + label[i][1]])
                    index += 1
                    if len(cizu) > 2:
                        for k in range(len(cizu) - 2):
                            out.append([toks[index], 'I-' + label[i][1]])
                            index += 1
                    out.append([toks[index], 'E-' + label[i][1]])
                    index += 1
                    break
                else:
                    out.append([toks[index], 'O'])
                    index += 1
    #split sentence by \n
    for i in out:
        if i == ['.', 'O']:
            outblank.append(i)
            outblank.append(['',''])
        else:
            outblank.append(i)
    for i in sorted(outblank, reverse=True):
        try:
            outblank.remove(['\n', 'O'])
        except ValueError:
            break
    return outblank
##############################
diraddress = infile
outaddress = outputfile
mkdir(outaddress)
trainfiles = json_load(diraddress)
#for i in range(len(trainfiles)):
#    text = trainfiles[i]['text']
#    denotation = trainfiles[i]['denotations']
#    spans, tokens = split_word(text)
#    output = trans_formal(spans, tokens, denotation)
q = 0
for info in os.listdir(diraddress):
    domain = os.path.abspath(diraddress)
    text = trainfiles[q]['text']
    denotation = trainfiles[q]['denotations']
    spans, tokens = split_word(text)
    output = trans_formal(spans, tokens, denotation)
    q += 1
    outfile = open(outaddress + '/' + info[:-5] + '.tab', 'w')
    for i in range(len(output)):
        outfile.write('%s\t%s\n'%(output[i][0], output[i][1]))
        #print(output[i][0])
    outfile.close()

print('transform json formate to BIOE:\nsuccessful!\n^_^\n#########################')
#print('done! ^_^')
