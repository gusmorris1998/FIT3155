# Name: Gus Morris
# Student ID: 30524526

from collections import deque
import bitarray
import sys

ALPHABET = 256

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, key, data):
        # Key data pairing, which we use when create the master node
        self.heap.append((key, data))
        # Heapify-up to maintain min-heap property
        self.heapifyUp(len(self.heap) - 1)

    def extractMin(self):
        if len(self.heap) == 0:
            return None
        # Swap the root (min element) with the last element
        minValue = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        # Heapify-down to maintain min-heap property
        self.heapifyDown(0)
        return minValue

    def heapifyUp(self, index):
        parentIndex = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parentIndex][0]:
            # Swap the child and parent if child is smaller
            self.heap[index], self.heap[parentIndex] = self.heap[parentIndex], self.heap[index]
            # Recursively heapify-up the parent index
            self.heapifyUp(parentIndex)

    def heapifyDown(self, index):
        leftChildIndex = 2 * index + 1
        rightChildIndex = 2 * index + 2
        smallest = index
        
        if leftChildIndex < len(self.heap) and self.heap[leftChildIndex][0] < self.heap[smallest][0]:
            smallest = leftChildIndex
        if rightChildIndex < len(self.heap) and self.heap[rightChildIndex][0] < self.heap[smallest][0]:
            smallest = rightChildIndex
        
        if smallest != index:
            # Swap the current index with the smallest child
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            # Recursively heapify-down the smallest index
            self.heapifyDown(smallest)

class Node:
    def __init__(self, char, value, left=None, right=None) -> None:
        self.char = char
        self.value = value
        self.left = left
        self.right = right

'''
End reference for the tree leafs as a result of python not being pass by reference
'''
class End:
    def __init__(self, end):
        self.end = end
'''
Simple node class that also contains a reference for suffix links
'''
class TreeNode:
    def __init__(self):
        self.edges = [None]*ALPHABET
        self.suffixLink = None

    def setEdge(self, char, edge):
        self.edges[ord(char)] = edge

    def returnEdge(self, char):
        return self.edges[ord(char)]

'''
Edges that exist after nodes, contains a start index and an end index
'''
class Edge:
    def __init__(self, start, end, suffixStart):
        self.suffixStart = suffixStart
        self.start = start
        self.end = end
        self.next = None

    def __len__(self):
        return self.end.end - self.start + 1

'''
Class that holds the components for Ukkonens algorithm
'''
class UkkonensAlgorithm:
    def __init__(self, string):
        # Add terminal chatacter
        self.string = string  + "$"
        self.root = TreeNode()
        # Global end leaf, extends for all that it is set
        self.GlobalEnd = End(-1)

        return self.suffixTreeConstruction()

    def suffixTreeConstruction(self):
        self.root.suffixLink = self.root
        n = len(self.string)
        activeNode, activeNodeEdge = self.root, None
        # implicit suffix tree phase
        i = 0
        # suffix extension index
        j = 0

        # The position of the tree in relation to the active nodes edge starting point and a
        # previous extension boolean for suffix link resolutions
        k, previousExtension = j, None

        while i < n:
            currentEdge = activeNode.returnEdge(self.string[k])
            # Extends the global end of all leafs with the 'reference'
            self.GlobalEnd.end = i

            iString, jString = self.string[:i], self.string[j:i]

            # No edge therefore Rule 2 extension
            if currentEdge == None:
                # Adds an edge corresponding to alphabet position. Only a single reference is changed, that being the global end, but this
                # Rule 2 extension
                activeNode.setEdge(self.string[k], Edge(k, self.GlobalEnd, j))
                if previousExtension:
                    # => There exists a previous extension
                    # Resolve the suffix link from the previous extension
                    previousExtension.suffixLink = activeNode
                    previousExtension = None
                
                # Link to the corresponding suffix link
                activeNode = activeNode.suffixLink

                if i == j:
                    i += 1
                    k = i
                    previousExtension = None
                j += 1
                continue

            iString, jString = self.string[:i], self.string[j:i]

            activeNodeEdge = currentEdge
            # If we consider our active node as u, this is 
            remainder = i - k + 1
            extendNode = False

            # Skip counting
            m = len(activeNodeEdge)
            # Conditional that checks that we have traversed further enough down our branch
            while remainder > len(activeNodeEdge):
                # Continously update our active node such that is the node before the extension
                activeNode = activeNodeEdge.next
                # How far down the brach we are
                k += len(activeNodeEdge)
                # What remains, checked against the conditional
                remainder -= len(activeNodeEdge)
                # Next edge along the traversal
                activeNodeEdge = activeNode.returnEdge(self.string[k])
                # If there exists no more edges along the way, signify to extend the branch of current node
                if activeNodeEdge is None:
                    extendNode = True
                    break
                     
            # There exists a current 
            if extendNode:
                continue
            
            iString, jString = self.string[:i], self.string[j:i]
            # The index at which either Rule 3 or ?? Rule 2 ?? will be aplied
            x = activeNodeEdge.start + remainder - 1 

            # if True => Rule 3, else split branch => Rule 2 case 1
            if self.string[x] == self.string[i]:
                if previousExtension:
                    previousExtension.suffixLink = activeNode
                previousExtension = None
                i += 1
                
                # Rule 3 has been applied => Showstopper rule, continue to next i
                continue

            # Rule 2, Case 1
            newNode = TreeNode()
            # Edge for the path that contains x != S[i+1]
            xPath = Edge(x, activeNodeEdge.end, activeNodeEdge.suffixStart)
            # Add S[i+1] to the edge set of new node

            newNode.setEdge(self.string[i], Edge(i, self.GlobalEnd, j))
            # Add the previous x-path to the newly created node
            newNode.setEdge(self.string[x], xPath)

            # Set the corresponding next edge and Suffix link to the root
            xPath.next = activeNodeEdge.next
            newNode.suffixLink = self.root

            # Set the corresponding values for the path leading up to x
            activeNodeEdge.end = End(x-1)
            activeNodeEdge.next = newNode
            activeNodeEdge.suffixStart = None

            # There exists a previous extension
            if previousExtension:
                # => resolve
                previousExtension.suffixLink = newNode

            # Set a previous extension that needs resolving
            previousExtension = newNode
            if activeNode is self.root:
                k += 1

            activeNode = activeNode.suffixLink            
            j += 1

def suffixArrayConstruction(word):
    # Algorithm runtime
    ukk = UkkonensAlgorithm(word)
    suffixArray = []
    # In-order traversal to get suffix starts
    collectSuffixArray(ukk.root, suffixArray)

    return suffixArray

def collectSuffixArray(treeNode, suffixArray):
    # Iterate through edges
    for edge in treeNode.edges:
        if edge is None:
            continue

        # appends the suffix start to suffix array 
        if edge.next is None:
            suffixArray.append(edge.suffixStart)
        # Recursively go down the tree
        else:
            collectSuffixArray(edge.next, suffixArray)

def bwtBasedEncoder(string):

    bitstring = ''
    # Replace with ukkonnen
    suffixArray = suffixArrayConstruction(string)
    bwt =  getBWT(suffixArray, string + '$')

    n = len(bwt)
    length  = eliasEncoding(n)
    bitstring += length

    occ = computeFrequencies(bwt)
    unique = eliasEncoding(len(occ.heap))
    bitstring += unique

    # Calculate Huffmann Codes
    huffmannRoot, huffmannCodes = calculateHuffmannCodes(occ)

    # Calculate 'data part'
    dataPart = calculateDataPart(huffmannCodes)
    bitstring += dataPart

    # Compute runlength encoding
    runlength = calculateRunlength(bwt, huffmannCodes)
    bitstring += runlength

    return bitstring

def calculateDataPart(charDict):
    bitstring = ''

    for key in charDict:
        if len(key) == 1:
            # This is done for $ character as it does not contain 7 bits, also removoes 0b
            _ascii = bin(ord(key))[2:].zfill(7)
            charCode = charDict[key]
            charCodelen = eliasEncoding(len(charCode))
            bitstring += _ascii + charCodelen + charCode

    return bitstring

def calculateRunlength(string, charDict):
    bitstring = ''
    n = len(string)
    j = 0

    while j < n:
        count = 1
        char = string[j]

        # Calculte run length of given character
        while (j+count) < len(string) and char == string[j + count]:
            count += 1
        
        # From huffmann dict
        charCode = charDict[char]
        # Via elias
        countCode = eliasEncoding(count)

        # Bitstring adds the 'tuple'
        bitstring += charCode + countCode

        j += count

    return bitstring

def calculateHuffmannCodes(freq):
        n = len(freq.heap)

        while n > 1:
            # This gets the node from the 2 highest frequencies
            left  = freq.extractMin()[1]
            right = freq.extractMin()[1]

            # return the frequency values of each node and add them together
            val = left.value + right.value
            # append the characters together
            char = left.char + right.char
            # Create new node with values
            node = Node(char, val, left, right)
            freq.insert(node.value, node)

            n = len(freq.heap)

        root = freq.extractMin()[1]
        huffmannCodes = shortestPathBFS(root)

        return root, huffmannCodes

def minimalBinaryCode(num):
    binary = ''
    quotient = num

    # Usual way to calculate binary from decimal
    while quotient:
        remainder = quotient % 2
        quotient = quotient // 2
        binary = str(remainder) +  binary

    return binary

def binaryToDecimal(bitstring):
    decimal = 0
    n = 0

    # Reversed so that we can iterate through forwards
    bitstring = bitstring[::-1]

    # Go through the reversed string. This is 
    for char in bitstring:
        if char == '1':
            decimal += 2**n

        n += 1
        
    return decimal


def eliasEncoding(num):
    mbc = minimalBinaryCode(num)
    encoding = mbc

    l = len(mbc) - 1

    while l > 0:
        lMBC = minimalBinaryCode(l).replace('1', '0', 1)
        encoding = lMBC + encoding
        # Calculate the new length
        l = len(lMBC) - 1

    return encoding

    
# Burrow Wheeler Transform ---------------------------------------------

def getBWT(suffixArray, string):
    res = []
    n = len(suffixArray)

    # Iterate over the suffix array, to get the cyclic index
    for element in suffixArray:
        index = (element - 1) % n
        res.append(string[index])

    return ''.join(res)

# Huffmann Encoding ------------------------------------------------------
"""
Variations of shortest path BFS which instead computes the bitstring rather
than the path
"""
def shortestPathBFS(root):
    if root is None:
        return {}

    # Initialize a queue for BFS
    queue = deque([root])

    bitDict = {root.char: ''}

    # Set to keep track of visited nodes
    visited = set()
    visited.add(root.char)

    while queue:
        # Dequeue a node
        currentNode = queue.popleft()

        currentBits = bitDict[currentNode.char]

        # Process the left child (if it exists and hasn't been visited)
        if currentNode.left and currentNode.left.char not in visited:
            bitDict[currentNode.left.char] = currentBits + '0'
            # Mark the left child as visited and add it to the queue
            visited.add(currentNode.left.char)
            queue.append(currentNode.left)

        # Process the right child (if it exists and hasn't been visited)
        if currentNode.right and currentNode.right.char not in visited:
            # Create the path to the right child
            bitDict[currentNode.right.char] = currentBits + '1'
            # Mark the right child as visited and add it to the queue
            visited.add(currentNode.right.char)
            queue.append(currentNode.right)

    # Return the dictionary containing the bits
    return bitDict
"""
Computes the frequencies of the characters in the algorithm and inserts them into an alphabet
"""
def computeFrequencies(string):
    n = len(string)
    occ = [None] * 256
    freq = MinHeap()

    # Frequencies into alphabet
    for char in string:
        try:
            occ[ord(char)] += 1
        except:
            occ[ord(char)] = 1

    # Creates the nodes for all those characters that have an occurrence
    for i in range(ALPHABET):
        if occ[i]:
            # Node contains the character and the number of occurrences
            node = Node(chr(i), occ[i])
            # Insert into the min heap, that we will use to create the master node later
            freq.insert(node.value, node)

    return freq


def huffmannEncoding(string):
    # Compute the frequencies of characters
    freq = computeFrequencies(string)
    n = len(freq.heap)

    while n > 1:

        # This gets the node from the 2 highest frequencies
        left  = freq.extractMin()[1]
        right = freq.extractMin()[1]

        # return the frequency values of each node and add them together
        val = left.value + right.value
        # append the characters together
        char = left.char + right.char
        # Create new node with values
        node = Node(char, val, left, right)
        freq.insert(node.value, node)

        n = len(freq.heap)

    # Extract root from min heap
    root = freq.extractMin()[1]
    # Get the dictionary for our huffmann encoding
    encodings = shortestPathBFS(root)
    compression = encodeString(string, encodings)

    return root, compression

def encodeString(string, encodings):
    bitstring = ''

    # Iterates through the characters and assigns encodings from dict
    for char in string:
        bitstring += encodings[char]

    return bitstring

def readFromFile(filePath):
    # Open the file in read mode
    with open(filePath, 'r') as file:
        # Read the entire contents of the file as a string
        fileContents = file.read()
    
    # Ukkonen takes string with out terminal character
    fileContents = fileContents.rstrip('$')

    # Return the contents of the file
    return fileContents

def writeToBinaryFile(filePath, binaryString):

    # Convert the binary string to bytes
    # Pad the binary string with leading zeros if necessary to make its length a multiple of 8
    length = len(binaryString)
    padding = (8 - length % 8) % 8
    # Adds padding to the right
    binaryString =  binaryString + '0' * padding

    bits = bitarray.bitarray(binaryString)

    # Write the bytes to the file
    with open(filePath, 'wb') as binFile:
        bits.tofile(binFile)

if __name__=="__main__":

    txt_file = sys.argv[1]
    string = readFromFile(txt_file)
    binarystring = bwtBasedEncoder(string)
    writeToBinaryFile('q2_encoder_output.bin', binarystring)
