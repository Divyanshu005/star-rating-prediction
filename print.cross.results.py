from __future__ import print_function
import sys
from os.path import exists

if len(sys.argv) < 2:
	sys.exit()

classifier = sys.argv[1]
percent = '100'
if len(sys.argv) > 2:
    percent = sys.argv[2]
experiments = ['']#['cv', '']
categories = ['books', 'restaurants', 'attractions', 'clothing_shoes_jewelry', 'home_kitchen', 'hotels', 'nightlife', 'event_planning_services', 'casinos', 'hairsalons', 'resorts', 'dentists']
features = {'cv': ['w2v'], '': ['w2v', 'w2v_and_phrases', 'w2v_and_posneg']}
metrics = ['mae', 'rmse']

expdone = 0
expall = 0
for metric in metrics:
	print(metric + '\n')
	print(',', end='')
	for experiment in experiments:
		for feature in features[experiment]:
			print(experiment.replace('cv', 'cv-') + feature + ',', end='')
	print('')
	for category in categories:
		print(category + ',', end='')
		for experiment in experiments:
			for feature in features[experiment]:
	                        done = 0
        	                mae = 0.0
                	        rmse = 0.0
                        	for i in range(0, 10):
                                        if percent != '100':
                                            filename = 'results/' + feature + '-' + classifier + '-' + category + '-' + experiment + str(i) + '-' + percent + 'p'
                                        else:
                                            filename = 'results/' + feature + '-' + classifier + '-' + category + '-' + experiment + str(i)
	                                if exists(filename):
                	                        done += 1
        	                                with open(filename, 'r') as fh:
                        	                        for line in fh:
                                	                        line = line.strip().split('\t')
                                        	                if line[0] == 'mae':
                                                	                mae += float(line[1])
                                                        	if line[0] == 'rmse':
                                                                	rmse += float(line[1])
				if done > 0:
					mae /= done
					rmse /= done
				star = ''
				if done < 10:
					star = '*'
				if metric == 'mae':
					print('%.3f' % mae, end='')
					print(star + ',', end='')
				if metric == 'rmse':
                                        print('%.3f' % rmse, end='') 
                                        print(star + ',', end='')

				expdone += done
				expall += 10
		print('')
	print('\n\n')

left = (expall - expdone) / 2
print(str(left) + ' experiments left.')
