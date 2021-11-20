# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 19:19:02 2021

Going OOP so I can reuse for later assignments
this is the node class

@author: Michael Nguyen 200860392
"""
import random
#needed for random node naming, dont want to confuse myself for anything "string" related
import string as strConts


class Node:  # takes layer # and node # as parameters for node naming
    def __init__(self, layerNumber=None, nodeNumber=None):
        self.layerNumber = layerNumber
        self.nodeNumber = nodeNumber
        self.children = []
        if layerNumber and nodeNumber is None:  # random node name if no parameter
            self.nodeName = ''.join(random.choice(  # 4 letter name mix of numbers or lowercase letters
                strConts.ascii_lowercase + strConts.digits) for i in range(4))
        else:  # node name is Node.L[Node Layer #]N[Node #]
            self.nodeName = 'Node.L' + str(layerNumber) + 'N' + str(nodeNumber)

        # weights of the connections to children initialized as blank list
        self.childrenConnectionWeights = []
        self.ID = ''.join(random.choice(  # TODO: delete after debugging
            strConts.ascii_lowercase + strConts.digits) for i in range(4))

    #recursively create children from node
    #takes current layer + and layer number map numbers as arguements
    def makeChildren(self, currLayer, numNodesPerLayerMap):
        #recursive exit when at last layer
        if currLayer == len(numNodesPerLayerMap)+1:
            return

        else:  # start/continue recursion
            # create children based on parameter for current layer
            for i in range(numNodesPerLayerMap[currLayer-1]):
                self.children.append(Node(currLayer, i))
            # use first node of current layer to create and connect to children of next layer
            tempFirstBorn = self.children[0]
            # recursive step in to create children for next layer
            tempFirstBorn.makeChildren((currLayer+1), numNodesPerLayerMap)
            # recursive step out to connect rest of layer nodes to next layer nodes
            for i in range(1, len(self.children)):
                self.children[i].children = tempFirstBorn.children[:]

    def adjustChildWeights(self):  # TODO; change for next assignment
        #recursive exit when at last node
        if not self.children:  # if list of children is empty, it is an end node
            return

        #for assigment 4, node connection weights are random
        self.childrenConnectionWeights == []
        for i in range(len(self.children)):  # recursively create random weights
            self.childrenConnectionWeights.append(random.uniform(0, 1))
            self.children[i].adjustChildWeights()  # recursive start

    def printChildren(self):
        #print indent based on layer
        print(self.layerNumber*'    ', end='')
        if not self.children:  # if list of children is empty, it is an end node
            print(self.nodeName)
        else:  # recursive node traversal
            print(self.nodeName + " is connected to:")
            #recursive step in
            for Node in self.children:
                Node.printChildren()

    def printWeight(self):
        #print indent based on layer
        print(self.layerNumber*'    ', end='')
        if not self.children:  # if list of children is empty, it is an end node
            print(self.nodeName)
        else:  # recursive node traversal
            print(self.nodeName + " is connected")
            # traversal by index and item
            for index, item in enumerate(self.children):
                print(item.layerNumber*'    ', end='')
                print("with weight " +
                      str(self.childrenConnectionWeights[index]) + " to:")
                item.printWeight()  # recursive start
