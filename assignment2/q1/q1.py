# Name: Gus Morris
# Student ID: 30524526

import sys
ALPHABET = 256

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

def computeRanks(string, positions):
    # string = readFromFile(stringFileName)
    suffixArray = suffixArrayConstruction(string)

    m = len(positions)
    n = len(suffixArray)
    
    # Assign array lengths accordingly so we can index
    outArray = [None] * m
    rankArray = [None] * n

    # Make the rank array. We do this so the rank can be indexed easily. O(n) time
    for i in range(n):
        rankArray[suffixArray[i]] = i

    # Index for the correspoding values of the positions. Notes positions arr is 1 indexed
    # and the output must be 1 indexed therefore -1 +1 added accordinly
    for j in range(m):
        outArray[j] = rankArray[positions[j] - 1] + 1

    writeArray(outArray, 'output_q1.txt')

    
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

def readFromFile(filePath):
    # Open the file in read mode
    with open(filePath, 'r') as file:
        # Read the entire contents of the file as a string
        fileContents = file.read()
    
    # Ukkonen takes string with out terminal character
    fileContents = fileContents.rstrip('$')

    # Return the contents of the file
    return fileContents

def readFileToArray(filePath):
    array = []
    
    # Open the file in read mode
    with open(filePath, 'r') as file:
        # Read each line in the file
        for line in file:
            # Strip any whitespace (e.g., newlines) from the line and convert it to a float
            # If your numbers are integers, you can use int(line.strip()) instead of float(line.strip())
            number = int(line.strip())
            # Append the number to the array
            array.append(number)
    
    return array


def writeArray(array, fileName):
    # Open the file in write mode
    with open(fileName, 'w') as file:
        # Iterate through each element in the array
        for element in array:
            # Write the element to the file, followed by a newline character
            file.write(str(element) + '\n')

if __name__=="__main__":

    stringFile = sys.argv[1]
    positionsFile = sys.argv[2]
    string = readFromFile(stringFile)
    positions = readFileToArray(positionsFile)
    computeRanks(string, positions)