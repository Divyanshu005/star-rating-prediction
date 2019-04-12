from __future__ import print_function
from os import listdir
from os.path import exists
import sys
import nltk
import json

if len(sys.argv) < 2:
    sys.exit()

number = sys.argv[1]
filt = ''
if len(sys.argv) > 2:
        filt = sys.argv[2]

for f in sorted(listdir('pos-' + number)):
    donecount = 0
    if not exists('phrases-' + number + '/' + f):
        if filt == '' or filt in f:
            with open('pos-' + number + '/' + f, 'r') as fh, open('phrases-' + number + '/' + f, 'wb') as fw:
                for line in fh:
                    donecount += 1

                    postags = json.loads(line)
                    segments = []
                    segments.append([])
                    segcount = 0
                    for a, b, c in postags:
                        if b not in ['CC', ',', '.', ';', ':']:
                            segments[segcount].append((a, b, c))
                        else:
                            segments.append([])
                            segcount += 1

                    phrases = []
                    for segment in segments:
                        for a, b, c in segment:
                            if c in ['pos', 'neg']:
                                for a2, b2, c2 in segment:
                                    if a2 != a and b2[0] in ['V', 'N']:
                                        phrases.append((a, a2))

                    phrasesjsonstr = json.dumps(phrases)
                    fw.write(phrasesjsonstr + '\n')

                    print(number + ' - ' + f + ': ' + str(donecount), end='\r')
            print(number + ' - ' + f + ': ' + str(donecount), end='\n')
