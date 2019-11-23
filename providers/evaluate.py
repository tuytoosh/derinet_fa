from providers.gather import GatherProvider

class EvaluateProvider:

    testRoute = ''
    def __init__(self):
        gather = GatherProvider()
        self.testRoute = gather.testRoute

    def clean(self, compound):
        return compound.replace('\u200c', '')

    def getAccuracy(self, rels, debug = False):
        # print('Evaluate.')
        test = open(self.testRoute)
        lines = test.read().split("\n")
        count = 0
        true = 0
        for l in lines:
            count += 1

            if len(l) < 1:
                break

            rel = l.split('-')
            if debug:
                print('-----------\n', rel[0], "\n", rel[1], "\n\n")
            if self.clean(rel[1]) in rels:
                if self.clean(rel[0]) in rels[rel[1]]:
                    true += 1
                    if debug:
                        print('true')
                else:
                    if debug:
                        print(rels[rel[1]])
            else:
                if debug:
                    print('not found')
            if debug:
                print('-----------------------\n')

        return true / count
