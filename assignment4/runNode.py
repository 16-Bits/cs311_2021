# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 20:31:24 2021

Going OOP so I can reuse for later assignments
this is the main class

@author: Michael Nguyen 200860392
"""
import node as myNode


def main():
    LAYER_NODE_COUNT = [4, 3, 2]  # based on assignment 4 graph
    nodeMaster = myNode.Node(0, 0)
    nodeMaster.makeChildren(1, LAYER_NODE_COUNT)
    nodeMaster.adjustChildWeights()
    nodeMaster.printChildren()
    nodeMaster.printWeight()


if __name__ == '__main__':
    main()
