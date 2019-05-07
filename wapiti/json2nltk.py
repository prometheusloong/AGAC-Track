# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:51:29 2019

@author: Pro
"""
import os
import re
import nltk
import json
nltk.data.path.append(r'/public/home/zcyu/ref/NLP/nltk_data')
trainfile = []
for info in os.listdir(r"/public/home/zcyu/ref/NLP/AGAC/AGAC_training"):
    domain = os.path.abspath(r"/public/home/zcyu/ref/NLP/AGAC/AGAC_training")
    info1 = os.path.join(domain,info)
    with open(info1) as f:
        data = json.load(f)
    trainfile.append(data)
    f.close()

def transformal(jsonid):
    global outblank
    out = []
    outblank = []
    text = trainfile[jsonid]['text']
    token = nltk.word_tokenize(text)
    denotation = trainfile[jsonid]['denotations']
    index = 0
    label = []
    for i in range(len(denotation)):
        label.append([text[denotation[i]['span']['begin']:denotation[i]['span']['end']], denotation[i]['obj']])
    
    for i in range(len(label)):
        testci = re.split(r' ', label[i][0])
        while index < len(token):
            if len(testci) == 1:
                if label[i][0] == token[index]:
                    out.append([token[index], 'B-' + label[i][1]])
                    index += 1
                    break
                else:
                    out.append([token[index], 'O'])
                    index += 1
            else:
                if testci[0] == token[index]:
                    out.append([token[index], 'B-' + label[i][1]])
                    index += 1
                    if len(testci) > 2:
                        for k in range(len(testci) - 2):
                            out.append([token[index], 'I-' + label[i][1]])
                            index += 1
                    out.append([token[index], 'E-' + label[i][1]])
                    index += 1
                    break
                else:
                    out.append([token[index], 'O'])
                    index += 1
    for i in out:
        if i == ['.', 'O']:
            outblank.append(i)
            outblank.append(['',''])
        else:
            outblank.append(i)
        
    return outblank

q = 0
#for q in range(len(trainfile)):
for info in os.listdir(r"/public/home/zcyu/ref/NLP/AGAC/AGAC_training"):
    domain = os.path.abspath(r"/public/home/zcyu/ref/NLP/AGAC/AGAC_training")
    transformal(q)
    q += 1
    outfile = open('/public/home/zcyu/ref/NLP/AGAC/outtrain/' + info[:-5] + '.tab', 'w')
    for i in range(len(outblank)):
        outfile.write('%s\t%s\n'%(outblank[i][0],outblank[i][1]))
        #print(transformal(q)[i][0])
    outfile.close()


print('done! ^_^')




