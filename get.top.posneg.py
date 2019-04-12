from __future__ import print_function
import json
import operator
import math
#from scipy.stats import entropy

categories = ['books', 'restaurants', 'attractions', 'clothing_shoes_jewelry', 'home_kitchen', 'hotels', 'nightlife', 'event_planning_services', 'casinos', 'hairsalons', 'resorts', 'dentists']

with open('toptuples.txt', 'wb') as fw:
    for category in categories:
        kld = {}
        toptuples = {'in': {}, 'out': {}}
        for i in range(0, 10):
            for star in range(1, 6):
                with open('posneg-' + str(i) + '/data-' + category + '-' + str(star) + '.jsonl', 'r') as fh:
                    for line in fh:
                        data = json.loads(line)
                        for em in ['neg', 'pos']:
                            for item in data[em]:
                                tup = item[0] + '--' + item[1]
                                toptuples['in'][tup] = 1 + toptuples['in'].get(tup, 0)
				toptuples['out'][tup] = 0

        for category2 in categories:
            if category != category2:
                for i in range(0, 10):
                    for star in range(1, 6):
                        with open('posneg-' + str(i) + '/data-' + category2 + '-' + str(star) + '.jsonl', 'r') as fh:
                            for line in fh:
                                data = json.loads(line)
                                for em in ['neg', 'pos']:
                                    for item in data[em]:
                                        tup = item[0] + '--' + item[1]
                                        if tup in toptuples['in']:
                                            toptuples['out'][tup] = 1 + toptuples['out'].get(tup, 0)

	intotal = sum(toptuples['in'].values())
        outtotal = sum(toptuples['out'].values())
        for tup, count in toptuples['in'].iteritems():
            pk = float(count) / intotal
            qk = float(toptuples['out'][tup]) / outtotal
            if count > 1000 and toptuples['out'][tup] > 0:
                kld[tup] = pk * math.log(pk / qk)

        sortedkld = sorted(kld.items(), key=operator.itemgetter(1), reverse=True)

        print(category + ':', end=' ')
        fw.write(category + ': ')
        printed = 0
        top = 5
        for tup, count in sortedkld:
            printed += 1
            if printed <= top:
                tokens = tup.split('--')
                print('(' + tokens[0] + ', ' + tokens[1] + ', ' + str(count) + ')', end=' ')
                fw.write('(' + tokens[0] + ', ' + tokens[1] + ', ' + str(count) + ') ')
        print('')
        fw.write('\n')
