import sys

NUM_CHARS = 256

def reverseBoyerMoore(patFile, txtFile):
    """
    Input: file containing text, file containing pattern
    Output: index set containing starting position of matches in text
    Implementation of the boyer-moore algoritm in reverse
    O(n/m) time complexity, O(1) space complexity
    """


    text, pat = readFrom(txtFile, patFile)
    n, m = len(text), len(pat)

    # Beginning index for pattern and text
    j = n - m

    bcDisplacement, gpDisplacement = 0, 0
    
    shiftTable = generateShiftTable(pat)
    goodPrefix = generateGoodPrefixTable(pat)
    matchedSuffix = generateMatchedSuffix(pat)
    indexSet = []

    while j - m > -1:
        k = 0

        while k != m and text[j + k] == pat[k]:
            k += 1

        # Every character of pat[0:m] has been checked against text [j: j+m]
        if k == m:
            # => Add to index set
            indexSet += [j]
            # j -= m - matchedSuffix[2]
            j -= 1

        # There was a mismatch after first character
        else:
            # --- BAD CHARACTER --- #
            # m-k corresponds to the table that contains left most occurrence for p[k+1:m]
            leftmostOccurrence = shiftTable[m-k-1][ord(text[j+k])]
            if leftmostOccurrence == None:
                # m-k is the remainder of the pattern, -------- remove comment maybe: +1 brings it past the bad character
                bcDisplacement = m-k
            # There exists and occurrence of the bad character in the unchecked part of the pattern
            elif leftmostOccurrence > k:
                # difference between the left most occurrence in L_k and k
                bcDisplacement = leftmostOccurrence-k
            else:
                bcDisplacement = 1
            # --- BAD CHARACTER --- #

            # --- GOOD PREFIX --- #
            # k > 0 conditional, not sure of necessity
            if k > 0 and goodPrefix[k-1] != 0:
                gpDisplacement = goodPrefix[k-1]
            # matched suffix, little unsure on this at the moment
            elif k > 0 and goodPrefix[k-1] == 0:
                gpDisplacement = m - matchedSuffix[k-1]
            # --- GOOD PREFIX --- #

            j -= max(bcDisplacement, gpDisplacement)
            bcDisplacement, gpDisplacement = 0,0
    
    # output
    sendOut(indexSet, "output_q1.txt")
        

def generateShiftTable(pattern):
    n = len(pattern)
    L_x = [NUM_CHARS * [None] for i in range(n)]
    # Iterating backwards here, so that left-most occurrence is updated
    for i in range(1, n):
        for j in range(n-1, (n-1)-i, -1):
            L_x[i][ord(pattern[j])] = j
    return L_x

def generateGoodPrefixTable(pat):
    m = len(pat)
    zTable = zAlgorithmGusfield(pat)
    goodPrefix = [0] * (m+1)

    for p in range(m-1, -1, -1):
        j = zTable[p]
        if j != 0:
            goodPrefix[j-1] = p

    return goodPrefix

def generateMatchedSuffix(pat):
    m = len(pat)
    
    zTable = zAlgorithmGusfield(pat)
    mp = [0] * m

    if zTable[m-1] + m-1 == m:
        mp[m-1] = 1

    for i in range(m-2, 0, -1):
        if zTable[i] + i == m:
            mp[i] = m - i
        else:
            mp[i] = mp[i+1]
    mp[0] = m

    return mp[::-1]
            
def zAlgorithmGusfield(S):

    # Setup
    l, r = 0, 0
    k, n = 1, len(S)
    Z = [0 for i in range(n)]

    # ----- base case ----- #
    i = 0
    while S[i] == S[i + 1]:
        Z[k] += 1
        i += 1

    if Z[k] > 0:
        r = Z[k]
        l = 1
    # ----- base case ----- #

    k += 1

    # ----- general cases ----- #
    while k < n:
        # ----- case 1: k > r ----- #
        if k > r:
            i = 0
            while k + i < n and S[i] == S[k + i]:
                Z[k] += 1
                i += 1
            if Z[k] > 0:
                l = k
                r = Z[k] + i - 1
            k += 1
        # ----- case 2: k >= r ----- #
        else:
            # ----- case 2a: ----- #
            if Z[k - l] < r - k + 1:
                Z[k] = Z[k - l]
            # ----- case 2a: ----- #
                
            # ----- case 2b: ----- #
            else:
                i = 0
                # Starts from the index after right-most position as we know all previous are correct
                while S[r + i + 1] == S[r - k + i + 2]:
                    i += 1
                Z[k] = Z[k - l] + i
                r = k + i - 1
                l = k
            # ----- case 2b: ----- #
            k += 1
    # ----- general cases ----- #
    
    return Z

def readFrom(file1, file2):
    file1 = open(file1, 'r')
    data1 = file1.read()
    file1.close()

    file2 = open(file2, 'r')
    data2 = file2.read()
    file2.close()
    return data1, data2


def sendOut(indexSet, outputFile):
    with open(outputFile, "w") as file:
        for k in indexSet:
            file.write(str(k) + "\n")

# if __name__ == '__main__':
#     #retrieve the file paths from the commandline arguments
#     _, filename1, filename2 = sys.argv
#     print("Number of arguments passed : ", len(sys.argv))

#     # since we know the program takes two arguments
#     print("First argument : ", filename1)
#     print("Second argument : ", filename2)
#     file1content = read_file(filename1)
#     print("\nContent of first file : ", file1content)
#     file2content = read_file(filename2)
#     print("\nContent of second file : ", file2content)


if __name__ == "__main__":

    txtFile = sys.argv[1]
    patFile = sys.argv[2]
    reverseBoyerMoore(patFile, txtFile)