import math
import sys

def run(alphabetSize, stringLength):
    alphabetSize, stringLength = int(alphabetSize), int(stringLength)
    greaterThanTwo = 0
    equalOne = 0
    equalN = 0

    n = alphabetSize**stringLength

    # Generate the alphabet
    alphabet = [chr(i) for i in range(ord('a'), ord('a') + alphabetSize)]

    if isPrime(stringLength):
        greaterThanTwo = n - alphabetSize
        equalN = n - alphabetSize
        equalOne = alphabetSize

        return commandLineOutput(alphabetSize, stringLength, greaterThanTwo, equalN, equalOne)
            
    # Generates the strings recursivily if alphabet size not prime
    def generateStrings(prefix, length):
        if length == 0:
            return [prefix]
        result = []
        for char in alphabet:
            result += generateStrings(prefix + char, length - 1)
        return result
    
    allStrings = generateStrings("", stringLength)

    # Generate all the cyclic rotations
    for text in allStrings:
        unique = uniqueCyclicRotations(text)

        if len(unique) == 1:
            equalOne += 1
        if len(unique) >= 2:
            greaterThanTwo += 1
        if len(unique) == stringLength:
            equalN += 1

    return commandLineOutput(alphabetSize, stringLength, greaterThanTwo, equalN, equalOne) 


def commandLineOutput(alphabetSize, stringLength ,greaterThanTwo, equalN, equalOne):
    print('Input Values:')
    print(str(alphabetSize) + ' ' + str(stringLength))
    print('Output:')
    print(str(greaterThanTwo) + ' ' + str(equalN) + ' ' + str(equalOne))

    if greaterThanTwo % stringLength == 0:
        print(True)
    else:
        print(False)

# Generates the cyclic rotations if needed
def uniqueCyclicRotations(string):
    n = len(string)
    rotations = set()

    for i in range(n):
        rotation = string[i:] + string[:i]
        rotations.add(rotation)
    
    return list(rotations)

# Basic prime finding algoirthm to calcute for alphabetSize
def isPrime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

if __name__=="__main__":

    alphabetSize = sys.argv[1]
    stringLength = sys.argv[2]
    run(alphabetSize, stringLength)