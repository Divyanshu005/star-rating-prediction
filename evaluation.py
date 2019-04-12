from os.path import join
import math

def confusion(id_preds, id_gts, testset, classifier):
  gts = []
  for m, c1 in id_gts.items():
    if not c1 in gts:
      gts.append(c1)

  gts = ['1', '2', '3', '4', '5']

  conf = {}
  for c1 in gts:
    conf[c1] = {}
    for c2 in gts:
      conf[c1][c2] = 0

  for tweetid, gt in id_gts.items():
    if tweetid in id_preds:
      pred = id_preds[tweetid]
    else:
      pred = 'neutral'
    conf[pred][gt] += 1

  print(''.ljust(12) + '  '.join(gts))

  for c1 in gts:
    print(c1.ljust(12)),
    for c2 in gts:
      if sum(conf[c1].values()) > 0:
        print('%.3f     ' % (conf[c1][c2] / float(sum(conf[c1].values())))),
      else:
        print('0.000     '),
    print('')

  print('')

def evaluate(id_preds, id_gts, outfile):
  mae = 0.
  rmse = 0.
  ncount = 0
  with open('predictions/' + outfile, 'wb') as fw:
    for revid, gt in id_gts.items():
      ncount += 1
      pred = id_preds[revid]
      fw.write(pred + '\t' + gt + '\n')

      mae += abs(float(gt) - float(pred))
      rmse += math.pow(float(gt) - float(pred), 2)

  mae = mae / ncount
  rmse = math.sqrt(rmse / ncount)
  with open('results/' + outfile, 'wb') as fw:
    fw.write('mae\t' + str(mae) + '\nrmse\t' + str(rmse))

  print(outfile + ': MAE - %.3f, RMSE - %.3f' % (mae, rmse))
