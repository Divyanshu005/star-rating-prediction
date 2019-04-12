from __future__ import print_function
from os import listdir
import sys
import nltk
import json
from os.path import exists

if len(sys.argv) < 2:
    sys.exit()

number = sys.argv[1]
filt = ''
if len(sys.argv) > 2:
    filt = sys.argv[2]

sentiment = {'pos': {}, 'neg': {}}
with open('opinion-lexicon-English/positive-words.txt', 'r') as fh:
    for word in fh.read().split():
        sentiment['pos'][word] = 1

with open('opinion-lexicon-English/negative-words.txt', 'r') as fh:
    for word in fh.read().split():
        sentiment['neg'][word] = 1

for f in sorted(listdir('review-data-sample-' + number)):
    donecount = 0
    if not exists('pos-' + number + '/' + f):
        if filt == '' or filt in f:
            linecount = 0
            with open('review-data-sample-' + number + '/' + f, 'r') as fh:
                for line in fh:
                    linecount += 1

            with open('review-data-sample-' + number + '/' + f, 'r') as fh, open('pos-' + number + '/' + f, 'wb') as fw:
                for line in fh:
                    donecount += 1

                    review = json.loads(line)
                    text = review['text']
                    postags = nltk.pos_tag(nltk.word_tokenize(text))

                    posjson = []
                    for a, b in postags:
                        sent = 'none'
                        if a.lower() in sentiment['pos']:
                            sent = 'pos'
                        elif a.lower() in sentiment['neg']:
                            sent = 'neg'
                        posjson.append((a, b, sent))
                    posjsonstr = json.dumps(posjson)

                    fw.write(posjsonstr + '\n')

                    print(number + ' - ' + f + ': ' + str(donecount) + ' / ' + str(linecount), end='\r')
            print(number + ' - ' + f + ': ' + str(donecount) + ' / ' + str(linecount), end='\n')
