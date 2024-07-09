import sys
from bitarray import bitarray

def bitMatch(txtFile, patFile):
    """
    Input: file containing text, file containing pattern
    Output: index set containing starting position of matches in text
    Exact bit matching algorithm via computation of delta, and previous bitvectors
    O(n*m) time complexity, O(m) space complexity
    """

    text, pat = readFrom(txtFile, patFile)

    n, m = len(text), len(pat)
    indexSet = []
     
    # edge case
    if m > n:
        return []

    # computation of the intial bitArray before iterating
    previous = bitarray([0] * m)
    for j in range(m):
        for i in range(m-j):
            if text[i+j] == pat[i]:
                bit = 0
            else:
                bit = 1
            compare = bit

            if compare == 1:
                previous[j] = 1

    # is the starting bitvector a match?
    if previous[0] == False:
        # yes => append to index set
        indexSet.append(0)

    # iterate through text
    for j in range(m, n):
        
        delta = bitarray()
        # Compute delta
        for i in range(m, 0, -1):
            if text[j] == pat[i-1]:
                bit = 0
            else:
                bit = 1
            delta.append(bit)
        

        # Compute current based on previous            
        shift = previous[1:]
        shift.append(False)
        # OR on the shift and delta
        current = shift | delta

        # if the pattern is a match, append the occurrence
        if current[0] == False:
            indexSet.append(j - m + 1)

        previous = current

    # output
    sendOut(indexSet, "output_q2.txt")


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

if __name__ == "__main__":

    txtFile = sys.argv[1]
    patFile = sys.argv[2]
    bitMatch(txtFile, patFile)