import copy
import re
import pprint

def readInput():
    # Read Sequence data file
    S = []
    Slines = []
    temp_1 = []
    listItem = []
    with open('data.txt', 'r') as Sfile:
        for line in Sfile:
            # Iterate every line and delete "\n" at the end of line
            Slines.append(line.rstrip('\n'))

        for line in Slines:
            # Remove "<" and ">"
            line = line.strip()[1:-1]
            # Split line base on "}{" after removing "{" and "}" before and after the line
            for s in re.split(r'}{', line[1:-1]):
                temp = [int(i) for i in re.split(', ', s)]
                # temp1 contain a sequence
                temp_1.append(temp)
            S.append(temp_1)
            temp_1 = []

    # Get all unique item in sequence
    for row in S:
        for elem in row:
            for item in elem:
               if item not in listItem:
                   listItem.append(item)
    listItem.sort()

    return S, listItem

def Gsp(S, listItem, minSup):
    CountMap = {}
    # Number of sequences
    for i in listItem:
        # Count transaction of each item
        count = 0
        for row in S:
            for elem in row:
                if (i in elem):
                    count = count + 1
                    # Add to dict
                    CountMap[i] = count
                    break

    L = init_pass(listItem, CountMap, minSup)
    
    # List of qualified item Level_1
    F1 = [i[0] for i in L]
    
    # Output file
    output_file = open("Output_GSP.txt", "w")
    output_file.write("The number of length: 1 sequential pattern is " + str(len(F1)) + "\n")
    for f in F1:
        print_s = "Pattern : <{" + str(f) + "}"
        print_s += ">"
        print_s += ": Count = " + str(CountMap[f])
        output_file.write(print_s + "\n")

    k = 2
    while (True):
        if k == 2:
            # Create level 2 candidate
            Ck = level_2(L)
        else:
            # Create level > 2 candidata
            Ck = MScandidateGen(Fk)

        # Count and save frequency
        SupCount = [0] * len(Ck)
        for c in range(len(Ck)):
            temp_count = 0
            for s in S:
                # Count number of Ck exist in transaction
                if Sub(Ck[c], s):
                    temp_count += 1
            SupCount[c] = temp_count
        
        # List contain sequence >=  minsup
        Fk = []
        # Add to dict with count
        Fk_withcount = []
        for c in range(len(Ck)):
            if SupCount[c] >= minSup:
                Fk.append(Ck[c])
                Fk_withcount.append([Ck[c], SupCount[c]])

        # No more candidate found then break
        if (len(Fk) == 0):
            break
        # Ouput value
        output_file.write("The number of length: " + str(k) + " sequential pattern is " + str(len(Fk)) + "\n")
        for f in Fk_withcount:
            print_s = "Pattern : <"
            for s in f[0]:
                print_s += "{"
                for i in s:
                    print_s += str(i) + ","
                print_s = print_s[:-1]
                print_s += "}"
            print_s += ">:Count = " + str(f[1])
            output_file.write(print_s + "\n")
        k += 1

# Check if i in Ck exist in s(transaction of sequence)
def Subset(Ck, s):
    for i in Ck:
        if i not in s:
            return False
    return True

# Check if Ck exist in s(sequence)
def Sub(Ck, s):
    counter = 0
    for i in Ck:
        isThere = False
        #  index of item if exist in sequence update from counter
        j = counter
        while j < len(s):
            # Iterate through every transaction in s
            if Subset(i, s[j]):
                isThere = True
                counter = j + 1
                break
            j += 1
        # If found nothing return False
        if not isThere:
            return False
    return True


# Return qualified level 1 candidates
def init_pass(M, CountMap, minSup):
    LMap = {}
    for i in M:
        if (CountMap[i] >= minSup):
            LMap[i] = CountMap[i]
    add_to_L = [[k, v] for k, v in LMap.items()]
    return add_to_L


# Generate level 2 candidates
def level_2(L):
    C2 = []
    for i in range(0, len(L)):
        # 2 exact same item in 2 transaction
        C2.append([[L[i][0]], [L[i][0]]])
        for j in range(i + 1, len(L)):
            if L[i][0] < L[j][0]:
                # 2 different item in 1 transaction
                C2.append([[L[i][0], L[j][0]]])
            else:
                C2.append([[L[j][0], L[i][0]]])
            # 2 different items in 2 transactions and reverse
            C2.append([[L[i][0]], [L[j][0]]])
            C2.append([[L[j][0]], [L[i][0]]])
    return C2


def MScandidateGen(F):
    C = []
    # Check last and first item
    for i in F:
        for j in F:
            s1 = i
            s2 = j
            #(s1, 0): Delete first item 
            #(s2, Length(s2) - 1): delete last item
            if (removeItem(s1, 0) == removeItem(s2, Length(s2) - 1)):
                # If last trasaction in s2 is 1 then add to C
                if (len(s2[-1]) == 1):
                    c1 = s1.copy()
                    c1.append(s2[-1])
                    C.append(c1)
                    
                else:
                # Replace last item of s1 with last item of s2
                    c1 = s1.copy()
                    del (c1[-1])
                    c1.append(s2[-1])
                    C.append(c1)
    return C


def removeItem(s, index):
    seqnew = copy.deepcopy(s)
    count = 0
    for element in seqnew:
        if count + len(element) <= index:
            count += len(element)
        else:
            del element[index - count]
            break

    return [element for element in seqnew if len(element) > 0]


def Length(s):
    l = 0
    for i in s:
        l += len(i)
    return l

if __name__ == '__main__':
    S, listItem = readInput()
    minSup = 3
    Gsp(S, listItem, minSup)