#!/usr/bin/env python
# -*- coding: utf-8 -*-
import testsets
import evaluation
import gensim
import re
import numpy as np
import json
import sys
from os.path import exists
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

def loadW2vModel():
    global model
    global num_features
    global index2word_set

#    model = gensim.models.KeyedVectors.load_word2vec_format('word2vec_twitter_model/word2vec_twitter_model.bin', binary=True, unicode_errors='ignore')
#    model = gensim.models.Word2Vec.load_word2vec_format('./w2v/GoogleNews-vectors-negative300.bin', binary=True)
    model = gensim.models.Word2Vec.load('./w2v/allstars')
    num_features = model.syn0.shape[1]
    index2word_set = set(model.index2word)

def makeFeatureVec(words, getsum = 0, useentropy = 0): # Function to average all of the word vectors in a given sentence, set getsum to 1 if sum wanted instead
    global model
    global num_features
    global index2word_set

    featureVec = np.zeros((num_features,),dtype="float32")
    nwords = 0.

    for word in words:
        if word != '' and word in index2word_set:
            if useentropy == 1:
                if word in entropies:
                    if entropies[word] < maxentropy:
                        purity = (maxentropy - entropies[word]) / maxentropy
                        nwords = nwords + purity
                        featureVec = np.add(featureVec, model[word] * purity)
            else:
                nwords = nwords + 1.
                featureVec = np.add(featureVec,model[word])

    if nwords > 0.0 and getsum == 0:
        featureVec = np.divide(featureVec,nwords)

    return featureVec

if len(sys.argv) < 5:
    sys.exit()

features = sys.argv[1] # unigrams, w2v, phrases, posneg, w2v_and_phrases, w2v_and_posneg
classifier = sys.argv[2] # svm, rf, maxent
testcategory = sys.argv[3] # see categories below
sampleid = sys.argv[4] # 0-9

outfile = features + '-' + classifier + '-' + testcategory + '-cv' + sampleid
if exists('results/' + outfile):
    sys.exit()

if features == 'w2v' or features == 'phrases' or features == 'w2v_and_phrases' or features == 'posneg' or features == 'w2v_and_posneg':
    loadW2vModel()

categories = ['attractions', 'books', 'casinos', 'clothing_shoes_jewelry', 'dentists', 'event_planning_services', 'hairsalons', 'home_kitchen', 'hotels', 'nightlife', 'resorts', 'restaurants']

datafeatures = {'train': [], 'test': []}
phrasefeatures = {'train': [], 'test': []}
posnegfeatures = {'train': [], 'test': []}
reviewids = {'train': [], 'test': []}
reviewgts = {'train': [], 'test': []}
idcounter = 0
texts = {'train': [], 'test': []}

if 'phrases' in features:
    for sid in range(0, 10):
        sampid = str(sid)
        dataset = 'train'
        if sampid == sampleid:
            dataset = 'test'
        for gt in range(1, 6):
            with open('cv/phrases-' + sampleid + '-' + sampid + '/data-' + testcategory + '-' + str(gt) + '.jsonl', 'r') as fh:
                for line in fh:
                    idcounter += 1
                    review = json.loads(line)
                    reviewids[dataset].append(str(idcounter))
                    reviewgts[dataset].append(str(gt))
                    phrasekeywords = []
                    for a, b in review:
                        phrasekeywords.append(a.lower())
                        phrasekeywords.append(b.lower())
                    phrasefeatures[dataset].append(makeFeatureVec(phrasekeywords))

if 'posneg' in features:
    for sid in range(0, 10):
        sampid = str(sid)
        dataset = 'train'
        if sampid == sampleid:
            dataset = 'test'
        for gt in range(1, 6):
            with open('cv/posneg-' + sampleid + '-' + sampid + '/data-' + testcategory + '-' + str(gt) + '.jsonl', 'r') as fh:
                for line in fh:
                    idcounter += 1
                    review = json.loads(line)
                    reviewids[dataset].append(str(idcounter))
                    reviewgts[dataset].append(str(gt))
                    vector = []
                    for sentiment in ['pos', 'neg']:
                        phrasekeywords = []
                        for a, b in review[sentiment]:
                            phrasekeywords.append(a.lower())
                            phrasekeywords.append(b.lower())
                        for w2vfeature in np.nditer(makeFeatureVec(phrasekeywords)):
                            vector.append(w2vfeature)
                    posnegfeatures[dataset].append(np.asarray(vector))

if features != 'posneg' and features != 'phrases':
    for sid in range(0, 10):
        sampid = str(sid)
        dataset = 'train'
        if sampid == sampleid:
            dataset = 'test'
        for gt in range(1, 6):
            with open('cv/review-data-sample-' + sampleid + '-' + sampid + '/data-' + testcategory + '-' + str(gt) + '.jsonl', 'r') as fh:
                for line in fh:
                    idcounter += 1
                    review = json.loads(line)
                    if not 'phrases' in features and not 'posneg' in features:
                        reviewids[dataset].append(str(idcounter))
                        reviewgts[dataset].append(str(gt))
                    text = re.sub(r'[^A-Za-z0-9 ]+', '', review['text'])
                    if features == 'w2v' or features == 'w2v_and_phrases' or features == 'w2v_and_posneg':
                        datafeatures[dataset].append(makeFeatureVec(text.lower().split()))
                    elif features == 'unigrams':
                        texts[dataset].append(text.lower())

if features == 'unigrams':
    ngram_vectorizer = CountVectorizer(ngram_range=(1, 1), token_pattern=r'\b\w+\b', max_features=50)
    X_train = ngram_vectorizer.fit_transform(texts['train'])
    del texts['train']
    X_test = ngram_vectorizer.transform(texts['test'])
    del texts['test']

if features == 'w2v_and_phrases':
    for index, item in enumerate(datafeatures['train']):
        feats = []
        for feat in np.nditer(datafeatures['train'][index]):
            feats.append(feat)
        for feat in np.nditer(phrasefeatures['train'][index]):
            feats.append(feat)
        datafeatures['train'][index] = np.asarray(feats)
    del phrasefeatures['train']

    for index, item in enumerate(datafeatures['test']):
        feats = []
        for feat in np.nditer(datafeatures['test'][index]):
            feats.append(feat)
        for feat in np.nditer(phrasefeatures['test'][index]):
            feats.append(feat)
        datafeatures['test'][index] = np.asarray(feats)
    del phrasefeatures['test']

if features == 'w2v_and_posneg':
    for index, item in enumerate(datafeatures['train']):
        feats = []
        for feat in np.nditer(datafeatures['train'][index]):
            feats.append(feat)
        for feat in np.nditer(posnegfeatures['train'][index]):
            feats.append(feat)
        datafeatures['train'][index] = np.asarray(feats)
    del posnegfeatures['train']

    for index, item in enumerate(datafeatures['test']):
        feats = []
        for feat in np.nditer(datafeatures['test'][index]):
            feats.append(feat)
        for feat in np.nditer(posnegfeatures['test'][index]):
            feats.append(feat)
        datafeatures['test'][index] = np.asarray(feats)
    del posnegfeatures['test']

if classifier == 'svm':
    mdl = LinearSVC(class_weight='balanced')
elif classifier == 'rf':
    mdl = RandomForestClassifier(class_weight='balanced')
elif classifier == 'maxent':
    mdl = LogisticRegression(class_weight='balanced')

if features == 'w2v' or features == 'w2v_and_phrases' or features == 'w2v_and_posneg':
    mdl.fit(datafeatures['train'], reviewgts['train'])
    del datafeatures['train']
elif features == 'phrases':
    mdl.fit(phrasefeatures['train'], reviewgts['train'])
    del phrasefeatures['train']
elif features == 'posneg':
    mdl.fit(posnegfeatures['train'], reviewgts['train'])
    del posnegfeatures['train']
elif features == 'unigrams':
    mdl.fit(X_train, reviewgts['train'])
    del X_train

id_preds = {}
id_gts = {}
if features == 'w2v' or features == 'w2v_and_phrases' or features == 'w2v_and_posneg':
    y_pred = mdl.predict(datafeatures['test'])
elif features == 'phrases':
    y_pred = mdl.predict(phrasefeatures['test'])
elif features == 'posneg':
    y_pred = mdl.predict(posnegfeatures['test'])
elif features == 'unigrams':
    y_pred = mdl.predict(X_test)

for k, reviewid in enumerate(reviewids['test']):
    id_preds[reviewid] = y_pred[k]
    id_gts[reviewid] = reviewgts['test'][k]

evaluation.evaluate(id_preds, id_gts, outfile)
