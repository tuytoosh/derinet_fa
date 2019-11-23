import sys

class CoreProvider:

    # just joins segments to create string from segments...
    def joiner(self, segs):
        return ''.join(segs)

    def expand(self, root, group, rels = {}, n = 2):
        root_str = self.joiner(root)
        tree = {}
        # add root
        tree[root_str] = {}
        tree[root_str]['root'] = root
        tree[root_str]['children'] = {}
        extra = []
        # if we are in last leaf, return empty children
        if len(group) == 0:
            return {}, {}, rels
        # when we add a node to tree we should remove it from group
        for_remove = []
        for g in group:
            if len(g) == n:
                # flag = true means that this node must add to `root`
                flag = True
                # direct check of overlap
                for i in range(0, n - 1):
                    if root[i] != g[i]:
                        flag = False
                        break
                # flag = false means in direct check we not get result and we need to check reverse...
                if flag == False:
                    flag = True
                    # reverse array elements
                    re_root = root[::-1]
                    re_g = g[::-1]
                    for i in range(0, n - 1):
                        if re_root[i] != re_g[i]:
                            flag = False
                            break
                # if there was any overlap add this node as child of root
                if flag == True:
                    tree[root_str]['children'][self.joiner(g)] = {'root': g}
                    tree[root_str]['children'][self.joiner(g)]['children'] = {}
                    j = self.joiner(g)
                    if j in rels:
                        rels[j].append(root_str)
                    else:
                        rels[j] = [root_str]
                    for_remove.append(g)
                else:
                    extra.append(g)
            else:
                extra.append(g)
        # remove all added children
        for rem in for_remove:
            group.remove(rem)
        new_tree = tree
        # foreach child of children do same...
        for child in list(tree[root_str]['children']):
            children, extra, rels = self.expand(tree[root_str]['children'][child]['root'], extra, rels, n + 1)
            if children != {}:
                new_tree[root_str]['children'][child] = children[child]
        return new_tree, extra, rels

    # gets a number as overlap of two array in direct and reverse browse and returns max of these two numbers
    def overlap(self, x, y):
        o_dir = 0
        o_rev = 0
        l = min(len(x), len(y))
        for i in range(l):
            if x[i] == y[i]:
                o_dir += 1
            else:
                break
        re_x = x[::-1]
        re_y = y[::-1]
        for i in range(l):
            if re_x[i] == re_y[i]:
                o_rev += 1
            else:
                break
        return max(o_dir, o_rev)

    # name of functions is confusing, this function gets extra and for each item of extra array, return best overlap and its overlap number
    def extract(self, tree, x, depth = 1):
        if(len(tree) == 0):
            return 0
        p = next(iter(tree.keys()))
        fathers = tree[p]['children'].keys()
        best_overlap = depth
        best_root = None
        for father in fathers:
            root = tree[p]['children'][father]['root']
            o = self.overlap(x, root)
            if o > best_overlap:
                best_overlap = o
                best_root = father
                bov, bro = self.extract({father: tree[p]['children'][father]}, x, o)
                if bov > best_overlap:
                    best_overlap = bov
                    best_root = bro
        return best_overlap, best_root

    # sets x as child of father in tree dictionary
    def set_father(self, tree, x, father):
        if(len(tree) == 0):
            return {}
        p = next(iter(tree.keys()))
        if p == father:
            tree[p]['children'][self.joiner(x)] = {}
            tree[p]['children'][self.joiner(x)]['root'] = x
            tree[p]['children'][self.joiner(x)]['children'] = {}

        else:
            fathers = tree[p]['children'].keys()
            for f in fathers:
                tree[p]['children'][f] = self.set_father({f: tree[p]['children'][f]}, x, father)
        return tree[p]

    def clean(self, str):
        return str.replace('\u200c', '')

    def render(self, groups):
        # print("Rendering.", end = '')
        rels = {}
        i = 0
        for word in groups:
            i += 1
            if i % 1000 == 0:
                # print('.', end = '')
                sys.stdout.flush()
            root = [word]
            group = groups[word].copy()
            if [word] in group:
                group.remove([word])
            if len(group) > 0:
                tree, extra, rels = self.expand(root, group)
                for x in extra:
                    father = self.extract(tree, x)
                    j = self.joiner(x)
                    if father[1] == None:
                        tree[word]['children'][self.joiner(x)] = {}
                        tree[word]['children'][self.joiner(x)]['root'] = x
                        tree[word]['children'][self.joiner(x)]['children'] = {}
                        if j in rels:
                            rels[j].append(word)
                        else:
                            rels[j] = [word]
                    else:
                        tree = {word: self.set_father(tree, x, father[1])}
                        if j in rels:
                            rels[j].append(father[1])
                        else:
                            rels[j] = [father[1]]
            else:
                tree = {word:{'root': root, 'children': {}}}
        return tree, rels
