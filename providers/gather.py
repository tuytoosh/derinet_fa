import operator
import morfessor
import sys
from os import path
from providers.data import DataProvider
from providers.core import CoreProvider

class GatherProvider:

    data = ''
    testRoute = 'data/test_set.txt'
    supSegmented = 'data/supSegmented.txt'
    unsupSegmented = 'data/unsupSegmented.txt'
    handSupSegmented = 'data/handSupSegmented.txt'
    handUnSupSegmented = 'data/handUnSupSegmented.txt'
    io = morfessor.MorfessorIO()
    def __init__(self):
        self.data = DataProvider()

    # just joins segments to create string from segments...
    def joiner(self, segs):
        return ''.join(segs)

    def clean(self, str):
        return str.replace('\u200c', '')

    def corpus(self, words):
        corpus = []
        for w in words:
            corpus += w
        return corpus

    def dictionary(self, corpus):
        return list(set(corpus))

    def stop(self, corpus, auto, count, morfessorData):
        # print('Stop.')
        freq = {}
        for c in corpus:
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1
        sorted_freq = sorted(freq.items(), key = operator.itemgetter(1), reverse = True)
        c = 1
        for f in sorted_freq[0:count]:
            print(c, f[1], f[0])
            c += 1
        stops = []
        if auto == True:
            for i in range(0 , count):
                stops.append (sorted_freq[i][0])
        else:
            exceptions = self.data.exceptions(morfessorData)
            for i in range(0, count):
                if i not in exceptions:
                    stops.append(sorted_freq[i][0])
        return stops

    def groups(self, words, stops):
        # print('Groups.', end = '')
        core = CoreProvider()
        groups = {}
        assignments = {}
        i = 0
        for w in words:
            i += 1
            if i % 1000 == 0:
                # print('.', end='')
                pass
            for m in w:
                if m not in stops:
                    if m in groups:
                        groups[m].append(w)
                    else:
                        groups[m] = [w]
                    j = core.joiner(w)
                    if j in assignments:
                        assignments[j].append(m)
                    else:
                        assignments[j] = [m]
        # print('\n')
        return groups.copy(), assignments.copy()

    def remSemi(self, rels):
        new_rels = {}
        for r in rels:
            clean_r = self.clean(r)
            new_rels[clean_r] = []
            for leaf in rels[r]:
                if self.clean(leaf) != '':
                    new_rels[clean_r].append(self.clean(leaf))
        del new_rels['']
        return new_rels

    def addTest(self, groups, assignments, supervised, hand):
        # print('Add Test', end = "")
        # sys.stdout.flush()

        if supervised and path.exists(self.supSegmented):
            return self.loadTest(supervised, groups, assignments, hand)

        if not supervised and path.exists(self.unsupSegmented):
            return self.loadTest(supervised, groups, assignments, hand)

        if supervised:
            segmented = open(self.supSegmented, 'w+')
        else:
            segmented = open(self.unsupSegmented, 'w+')

        test = open(self.testRoute)
        lines = test.read().split("\n")
        i = 0;
        for l in lines:
            if i % 10 == 0:
                # print('.', end='')
                sys.stdout.flush()
            i += 1
            rel = l.split('-')

            for compound in rel:
                if compound not in assignments:
                    parts = self.segment(compound, supervised)
                    segmented.write(' '.join(parts) + "\n")
                    for m in parts:
                        if m in groups:
                            groups[m].append(parts)
                        else:
                            groups[m] = [parts]

                        if compound in assignments:
                            assignments[compound].append(m)
                        else:
                            assignments[compound] = [m]
        # print("\n")
        segmented.close()
        return groups, assignments

    def loadTest(self, supervised, groups, assignments, hand):
        if supervised:
            if hand:
                test = open(self.handSupSegmented)
            else:
                test = open(self.supSegmented)
        else:
            if hand:
                test = open(self.handUnSupSegmented)
            else:
                test = open(self.unsupSegmented)

        lines = test.read().split("\n")
        for l in lines:
            parts = l.split(' ')
            compound = self.joiner(parts)
            for m in parts:
                if m in groups:
                    groups[m].append(parts)
                else:
                    groups[m] = [parts]

                if compound in assignments:
                    assignments[compound].append(m)
                else:
                    assignments[compound] = [m]
        return groups, assignments

    def segment(self, compound, supervised):
        if supervised:
            model = self.io.read_binary_model_file('data/supervised.bin')
        else:
            model = self.io.read_binary_model_file('data/unsupervised.bin')
        return model.viterbi_segment(compound)[0]
