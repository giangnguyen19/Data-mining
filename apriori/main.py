import pandas as pd
import itertools
import pprint

class apriori():
    def __init__(self, items, records,  minSup):


        def stage_1(items, minSup):
            # level 1 candidate
            c1 = {i:items.count(i) for i in items}
            l1 = {}
            #  add qualified candidate to l1
            for key, value in c1.items():
                if value >= minSup:
                    l1[key] = value 
   
            return c1, l1

        def stage_2(l1, records, minSup):
            l1 = sorted(list(l1.keys()))
            #  Get all permutation for level 2 candidate from qualified level 1
            L1 = list(itertools.combinations(l1, 2))

            c2 = {}
            l2 = {}
            for iter1 in L1:
                count = 0
                for iter2 in records:
                    if sublist(iter1, iter2):
                        count+=1
                c2[iter1] = count
            for key, value in c2.items():
                if value >= minSup:
                    # if check_subset_frequency(key, l1, 1):
                        l2[key] = value 

            return c2, l2
            
        def stage_3(l2, records, minSup):
            l2 = list(l2.keys())
            L2 = sorted(list(set([item for t in l2 for item in t])))
            L2 = list(itertools.combinations(L2, 3))
            c3 = {}
            l3 = {}
            for iter1 in L2:
                count = 0
                for iter2 in records:
                    if sublist(iter1, iter2):
                        count+=1
                c3[iter1] = count
            for key, value in c3.items():
                if value >= minSup:
                    l3[key] = value 

            
            return c3, l3

        def stage_4(l3, records, minSup):
            l3 = list(l3.keys())
            L3 = sorted(list(set([item for t in l3 for item in t])))
            L3 = list(itertools.combinations(L3, 4))
            c4 = {}
            l4 = {}
            for iter1 in L3:
                count = 0
                for iter2 in records:
                    if sublist(iter1, iter2):
                        count+=1
                c4[iter1] = count
            for key, value in c4.items():
                if value >= minSup:
                    l4[key] = value 
                
            return c4, l4

        # Check if lst1 in lst2
        def sublist(lst1, lst2):
            return set(lst1) <= set(lst2)
            

        c1, l1 = stage_1(items, minSup)
        c2, l2 = stage_2(l1, records, minSup)
        c3, l3 = stage_3(l2, records, minSup)
        c4, l4 = stage_4(l3, records, minSup)


        # Output file
        hold = [l1,l2,l3,l4]
        output_file = open("Output_Apriori.txt", "w")
        for s,i in enumerate(hold):
            output_file.write("The number of length: " + str(s+1)+ '\n')
            for key, value in i.items():
                print_s = "Pattern : {" + str(key) + "}"
                print_s += ": Count = " + str(value)
                output_file.write(print_s + "\n")

if __name__ == '__main__':
    
    minSup = 2
    records = [['A', 'C', 'B'],
                ['C', 'A', 'B', 'D'],
                ['C', 'E', 'F'],
                ['G', 'I', 'C', 'A'],
                ['I', 'E', 'B'],
                ['C', 'E', 'F'],
                ['I', 'E', 'D'],
                ['I', 'C', 'E', 'B'],
                ['G', 'I', 'C', 'E'],
                ['C', 'A'],
                ['J', 'H', 'B', 'D'],
                ['J', 'H', 'B', 'D'],
                ['J', 'U', 'F'],
                ['C', 'J', 'H'],
                ['C', 'U', 'B'],
                ['J', 'U', 'D'],
                ['C', 'U', 'F'],
                ['C', 'J', 'U'],
                ['C', 'J', 'U'],
                ['E', 'A', 'J', 'D']]
    
    # Add itemsets to records for better manipulation
    # List all items then sort 
    items = sorted([item for sublist in records for item in sublist if item != 'nan'])
    apriori(items, records, minSup)