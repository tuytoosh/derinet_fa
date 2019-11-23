import operator
import sys
from providers.data import DataProvider
from providers.gather import GatherProvider
from providers.core import CoreProvider
from providers.evaluate import EvaluateProvider

dataProvider = DataProvider()
gatherProvider = GatherProvider()
coreProvider = CoreProvider()
evaluateProvider = EvaluateProvider()

morfessorData = sys.argv[1] in ['y', 'yes', 'True']
auto = sys.argv[2] in ['y', 'yes', 'True']
count = int(sys.argv[3])
supervised = sys.argv[4] in ['y', 'yes', 'True']


fmt = "{morfessorData}\t{auto}\t{count}\t{supervised}\t{Accuracy:.3f}"
words, segmentations = dataProvider.get(morfessorData)

corpus = gatherProvider.corpus(words)
dictionary = gatherProvider.dictionary(corpus)

stops = gatherProvider.stop(corpus, auto, count, morfessorData)
groups, assignments = gatherProvider.groups(words, stops)
groups, assignments = gatherProvider.addTest(groups, assignments, supervised, False)
tree, rels = coreProvider.render(groups)
rels = gatherProvider.remSemi(rels)
Accuracy = evaluateProvider.getAccuracy(rels)
print(fmt.format(morfessorData = morfessorData, auto = auto, count = count, supervised = supervised, Accuracy = Accuracy))

print('Output Route: ' + dataProvider.write_ufal_format(rels, segmentations))
