import sys

def run(inputFile, commandFile, t):
    t = int(t)
    words = readFileToArray(inputFile)
    tree = BTree(t, words.pop(0))

    for word in words:
        tree.insert(word)

    list = tree.outputInorder()

    with open(commandFile, 'r') as file:
        for line in file:
            line.strip()
            (command, word) = line.split()

            match command:
                case 'insert':
                    tree.insert(word)
                case 'delete':
                    tree.delete(word)

    order = tree.outputInorder()
    writeArray(order, 'output_q2.txt')

    return list


class BTree:
    def __init__(self, t, key) -> None:
        self.root = Node([key], [None, None], self)
        self.t = t

        self.root.isRoot = True
        self.root.isLeaf = True
        self.order = []

    def insert(self, key):
        if self.root.capacity == 2 * self.t - 1:
            node = self.root.splitNode(None)
            # So we know we will be starting from a root that is not full
            return node.insertAux(key)

        self.root.insertAux(key)

    def delete(self, key):
        self.root.deleteAux(key)

    def searchTree(self, key):
        return self.root.searchAux(key)

    def outputInorder(self):
        self.order = []
        self.root.getOrder()

        return self.order


class Node:
    def __init__(self, keys, pointers, tree) -> None:
        self.keys = keys
        self.pointers = pointers
        self.tree = tree
        self.capacity = len(keys)
        self.parentNode = None
        self.isLeaf = False

    def getOrder(self):
        # self.tree = tree
        tree = self.tree
        if self.isLeaf:
            tree.order += self.keys
            return
        
        for i in range(self.capacity):
            node = self.pointers[i]
            if node is not None:
                node.getOrder()
            tree.order += [self.keys[i]]

        node = self.pointers[self.capacity]
        if node is not None:
            node.getOrder()

    def setChildren(self, nodes):
        for node in nodes:
            if not node is None:
                node.setParent(self)

    def setParent(self, node):
        self.parentNode = node

    def searchAux(self, key):
        inNode, index = binarySearch(self.keys, key)

        if inNode:
            return True

        if not self.isLeaf:
            child = self.pointers[index]
            if child is None:
                return False
            else:
                return child.searchAux(key)
        
        return False

    def insertAux(self, key):
        _, index = binarySearch(self.keys, key)
        if _:
            return

        t = self.tree.t

        if self.isLeaf:
            return self.insertKey(key, index)
                    
        childNode = self.pointers[index]
        if childNode.capacity == 2*t - 1:
            node = childNode.splitNode(index)
            node.insertAux(key)
        else:
            childNode.insertAux(key)

    def deleteAux(self, key):
        inNode, index = binarySearch(self.keys, key)
        t = self.tree.t

        # Case 1 deletion
        if self.isLeaf:
            if inNode:
                self.keys.pop(index)
                self.pointers.pop(index)
                self.capacity -= 1
            return
        
        left = False
        
        # Case 2:
        if inNode:
            foundKey = self.keys[index]
            leftChild = self.pointers[index]
            rightChild = self.pointers[index + 1]
            # find in order predecessor
            if leftChild.capacity > t - 1:
                predIndex = leftChild.capacity - 1
                leftChildKey = leftChild.keys[predIndex]
                leftChild.keys[predIndex] = foundKey
                self.keys[index] = leftChildKey

                return leftChild.deleteAux(key)
            # find in order successor
            elif rightChild.capacity > t - 1:
                succIndex = 0
                rightChildKey = rightChild.keys[succIndex]
                rightChild.keys[succIndex] = foundKey
                self.keys[index] = rightChildKey

                return rightChild.deleteAux(key)
            # Both children == t - 1 => merge
            else:
                mergedNode = self.mergeSiblings(index)
                return mergedNode.deleteAux(key, left)


        childNode = self.pointers[index]
        # Case 3:
        if childNode.capacity == t - 1:
            try:
                # Try and index right sibling first
                immediateSibling = self.pointers[index + 1]
            except:
                # There must be a left sibling:
                immediateSibling = self.pointers[index - 1]
                # Set flag to indicate for rotation direction
                left = True
            if immediateSibling.capacity > t - 1:
                self.rotateChildren(index, left)
            else:
                mergedNode = self.mergeSiblings(index, left)
                return mergedNode.deleteAux(key)
            self.deleteAux(key)
        else:
            childNode.deleteAux(key)


    def rotateChildren(self, index, left):
        # Coming from the left or right immediate sibling
        if left:
            childNode = self.pointers[index]
            leftChildSibling = self.pointers[index - 1]

            parentKey = self.keys[index - 1]
            leftChildSiblingKey = leftChildSibling.keys[leftChildSibling.capacity - 1]
            leftChildSiblingPointer = leftChildSibling.pointers[leftChildSibling.capacity]

            # Update values
            leftChildSibling.keys.pop()
            leftChildSibling.pointers.pop()
            leftChildSibling.capacity -= 1

            childNode.keys.insert(0, parentKey)
            childNode.pointers.insert(0, leftChildSiblingPointer)
            childNode.capacity += 1
            self.key[index - 1] = leftChildSiblingKey
        else:
            childNode = self.pointers[index]
            rightChildSibling = self.pointers[index + 1]

            parentKey = self.keys[index]
            rightChildSiblingKey = rightChildSibling.keys[0]
            rightChildSiblingPointer = rightChildSibling.pointers[0]

            rightChildSibling.keys.pop(0)
            rightChildSibling.pointers.pop(0)
            rightChildSibling.capacity -= 1

            childNode.keys.append(parentKey)
            childNode.pointers.append(rightChildSiblingPointer)
            childNode.capacity += 1
            self.keys[index] = rightChildSiblingKey

    def mergeSiblings(self, index, left):
        if left:
            index -= 1

        leftChild, rightChild = self.pointers[index], self.pointers[index + 1]
        parentKey = self.keys[index]

        mergedKeys = leftChild.keys + [parentKey] + rightChild.keys
        mergedPointers = leftChild.pointers + rightChild.pointers

        mergedNode = Node(mergedKeys, mergedPointers, self.tree)

        self.keys.pop(index)
        self.pointers[index] = mergedNode
        self.pointers.pop(index + 1)
        self.capacity -= 1

        # Reassign root if root had capacity 1 and got merged into the children
        if self.capacity == 0:
            self.tree.root = mergedNode
        # Otherwise assign parent node
        else:
            mergedNode.parentNode = self
        return mergedNode

    def insertKey(self, key, index):
        self.keys.insert(index, key)
        self.pointers.append(None)
        self.capacity += 1

    def splitNode(self, parentPointerIndex):
        medianIndex = self.capacity // 2
        parentNode = self.parentNode
        
        # 2t - 1 will always be odd therefore spread evenly between left and right
        keysLeft = self.keys[0:medianIndex]
        keysRight = self.keys[medianIndex + 1:]
        medianKey = self.keys[medianIndex]

        # 2t pointers will always be distributed between left and right node
        pointersLeft = self.pointers[0:medianIndex + 1]
        pointersRight = self.pointers[medianIndex + 1:]

        # Create two new nodes
        leftNode = Node(keysLeft, pointersLeft, self.tree)
        rightNode = Node(keysRight, pointersRight, self.tree)

        # Leaf membership preserved on left and right split Nodes
        if self.isLeaf:
            leftNode.isLeaf = True
            rightNode.isLeaf = True

        # Is root node?
        if parentPointerIndex is None:
            newRoot = Node([medianKey], [leftNode, rightNode], self.tree)
            self.tree.root = newRoot

            # Set parent values accordingly
            leftNode.setParent(newRoot)
            leftNode.setChildren(pointersLeft)
            rightNode.setParent(newRoot)
            rightNode.setChildren(pointersRight)


            return newRoot

        # Middle insertion
        else:
            # Insert key
            parentNode.keys.insert(parentPointerIndex, medianKey)
            parentNode.capacity += 1

            # Delete old link and insert new pointers to left and right
            parentNode.pointers.pop(parentPointerIndex)
            parentNode.pointers.insert(parentPointerIndex, rightNode)
            parentNode.pointers.insert(parentPointerIndex, leftNode)

            # Set parent values accordingly
            leftNode.setParent(parentNode)
            leftNode.setChildren(pointersLeft)
            rightNode.setParent(parentNode)
            rightNode.setChildren(pointersRight)

            return parentNode

def binarySearch(array, element):
    low, high = 0, len(array)

    while low <= high:
        middle = (low + high) // 2
        
        try:
            if array[middle] < element:
                low = middle + 1
            elif array[middle] > element:
                high = middle - 1
            else:
                return True, middle
        except IndexError:
            return False, middle
    
    if array[middle] < element:
        return False, middle + 1
    if array[middle] > element:
        return False, middle
    
def readFileToArray(filePath):
    array = []
    
    # Open the file in read mode
    with open(filePath, 'r') as file:
        # Read each line in the file
        for line in file:
            # Strip any whitespace (e.g., newlines) from the line and convert it to a float
            # Append the number to the array
            array.append(line.strip())
    
    return array

def writeArray(array, fileName):
    # Open the file in write mode
    with open(fileName, 'w') as file:
        # Iterate through each element in the array
        for element in array:
            # Write the element to the file, followed by a newline character
            file.write(element + '\n')


if __name__=="__main__":

    t = sys.argv[1]
    inputFile = sys.argv[2]
    commandFile = sys.argv[3]
    run(inputFile, commandFile, t)