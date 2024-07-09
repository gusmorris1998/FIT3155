from collections import deque
import bitarray
import sys

ALPHABET = 256

def readBinFile(fileName):
    bits = bitarray.bitarray()

    with open(fileName, "rb") as file:
        bits.fromfile(file)

    bitstring = bits.to01()

    return bitstring

def bwtBasedDecoder(fileName):

    bitstring = readBinFile(fileName)

    i = 0
    # Get the string length
    strLen, j = eliasDecoding(bitstring[i:])
    i += j
    # Get the number of unique characters
    unique, j = eliasDecoding(bitstring[i:])
    i += j
    # Decode the data part
    codeDict, j, maxCodeLen = decodeDataPart(bitstring[i:], unique)
    i += j
    # Decode the runlength
    decodedString = decodeRunLen(bitstring[i:], codeDict, maxCodeLen, strLen)
    # Invert the BWT
    decodedString = invertBWT(decodedString)

    return decodedString

def decodeRunLen(bitstring, codeDict, maxCodeLen, strLen):
    n = len(bitstring)
    string = ''
    i = 0

    # Either we iterate through entire bit string or we reach the number of characters
    # previosuly computed for out string length
    while i < n and len(string) < strLen:
        j = 0
        # Huffmann codes all end in 0 except for the strings of 1*max length
        while bitstring[i + j] != '0' and j != maxCodeLen - 1:
            j += 1
        # Previous loop calculates the huffmann code
        char = codeDict[bitstring[i:i+j+1]]

        i += j + 1
        # Simple runlength decoding
        runlength, add = eliasDecoding(bitstring[i:])
        string += char * runlength

        i += add

    return string
    
def decodeDataPart(string, n):
    i, j = 0, 0
    maxCodeLen = 0
    codeDict = {}

    while j < n:
        # Character comes first
        _ascii = chr(binaryToDecimal(string[i:i+7]))
        i += 7

        # then code length
        charCodeLen, h = eliasDecoding(string[i:])
        i += h
        # then chacter code
        charCode = string[i:i+charCodeLen]
        codeDict[charCode] = _ascii

        i += charCodeLen
        j += 1

        # Max code length will be used further in the decoding steps
        if charCodeLen > maxCodeLen:
            maxCodeLen = charCodeLen

    end = i

    return codeDict, end, maxCodeLen


def eliasDecoding(bitstring):
    # Edge case
    if bitstring[0] == '1':
        return 1, 1

    i = 1
    m = 2

    # if == 0, still decoding length parts
    while bitstring[i] == '0':
        previousM = m
        # flip bit of first to 1 to calculate length
        m = binaryToDecimal('1' + bitstring[i+1:i+m]) + 1
        i += previousM
    end = i + m
    # Important to not just run [i:], as consecutive elias codes cannot be computed
    decoding = binaryToDecimal(bitstring[i:i+m])

    return decoding, end

def minimalBinaryCode(num):
    binary = ''
    quotient = num

    while quotient:
        remainder = quotient % 2
        quotient = quotient // 2
        binary = binary + str(remainder)

    return binary

def binaryToDecimal(bitstring):
    decimal = 0
    n = 0

   # String is reversed here so that can run through the characters positively and calculate
    bitstring = bitstring[::-1]

    for char in bitstring:
        if char == '1':
            decimal += 2**n

        n += 1
        
    return decimal


def invertBWT(bwt):
    n= len(bwt) - 1
    result = [None] * n 
    rank, occurrences = [None] * ALPHABET, [None] * len(bwt)

    # How many times each character occurs
    for i, char in enumerate(bwt):
        if char == "$":
            rank[0], occurrences[i] = 1, 0
            continue

        index = ord(char)
        
        if rank[index] is None:
            rank[index], occurrences[i] = 1, 0
        else:
            occurrences[i] = rank[index]
            rank[index] += 1

    # Count keeping track of the rank
    count = 0
    for i in range(len(rank)):

        if rank[i] is not None:
            value = rank[i]
            rank[i] = count
            count += value

    i = n - 1
    nextI = 0
    char = bwt[nextI]

    # indictates we have inverted
    while char != "$":
        result[i] = char
        nextI = rank[ord(char)] + occurrences[nextI]
        char = bwt[nextI]
        i -= 1
    
    # result in a list of characters => join
    return ''.join(result)

def sendOut(string, outputFile):
    with open(outputFile, "w") as file:
        file.write(string)

if __name__=="__main__":
    binFile = sys.argv[1]
    string = bwtBasedDecoder(binFile) + '$'
    sendOut(string, 'q2_decoder_output.txt')

