from pprint import pprint
from typing import *
from collections import defaultdict
import pprint

def invertedindex(seqs, entries = None):
    index = defaultdict(list)
    
    for k, seq in enumerate(seqs):
        i, lastpos = entries[k] if entries else (k, -1)
        # Iterate throught every item in each row
        for p, item in enumerate(seq, start=(lastpos + 1)):
            l = index[item]
            # Check if meet item on the same row that is already added, continue to next row
            if len(l) and l[-1][0] == i:
                continue

            l.append((i, p))
    return index


def nextentries(data, entries):
    return invertedindex((data[i][lastpos + 1:] for i, lastpos in entries),entries)
    
class bide_alg:
    
    def __init__(self, db, minsup, maxlen):
        
        self._db = db
        self.minsup = minsup
        self.maxlen = maxlen
        self._results = []
    
    def __reversescan(self, db, patt, matches, check_type):
        # db: complete database
        # patt: the current pattern
        # matches: a list of tuples (row_index, the index of the last element of patt within db[row_index])
        def islocalclosed(previtem):
            closeditems = set()
            
            for k, (i, endpos) in enumerate(matches):
                localitems = set()
                
                for startpos in range(endpos-1, -1, -1):
                    item = db[i][startpos]
                    # if found matches save it index to matches variable
                    if item == previtem:
                        matches[k] = (i, startpos)
                        break
                    
                    localitems.add(item)
                
                # first run: add elements of localitems to closeditems
                # after first run: start intersection
                (closeditems.update if k==0 else closeditems.intersection_update)(localitems)
            return len(closeditems) > 0
            
        check = True if check_type == 'closed' else False
        for previtem in reversed(patt[:-1]):

            if islocalclosed(previtem):
                check = False if check_type == 'closed' else True
                break
        return check
        
    
    def isclosed(self, db, patt, matches):
        
        return self.__reversescan(db, [None, *patt, None], [(i, len(db[i])) for i, _ in matches], 'closed')
    

        
    
    def bide_frequent_rec(self, patt, matches):
        sup = len(matches)
        # if pattern's length is greater than minimum length
        if len(patt) >= 0:
            # if pattern's support < minsup, stop
            if sup < self.minsup:
                return None
            # backward extension check
            if self.isclosed(self._db, patt, matches):
                self._results.append((patt, sup))

            
        # find the following items
        occurs = nextentries(self._db, matches)
        for newitem, newmatches in occurs.items():
            # set the new pattern
            newpatt = patt + [newitem]
            # forward extension check 
            if (len(matches) == len(newmatches)) and ((patt, sup) in self._results):
                self._results.remove((patt, sup))

            self.bide_frequent_rec(newpatt, newmatches)
    def _mine(self):
        self.bide_frequent_rec([], [(i, -1) for i in range(len(self._db))])    


if __name__ == "__main__":
    db = [['c', 'a', 'a', 'b', 'c'],
    ['a', 'b', 'c', 'b'],
    ['c', 'a', 'b', 'c'],
    ['a', 'b', 'b', 'c', 'a']]

    # Get longest sequence
    max = max([len(row) for row in db])

    bide_obj = bide_alg(db, 2 , max)
    bide_obj._mine()
    pprint.pprint(bide_obj._results)