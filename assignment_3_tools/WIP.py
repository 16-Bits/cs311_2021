# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 07:03:27 2021

@author: 16-Bit
"""
import argparse
import random
import json

def main():
    #arguement parameter parsing to get info
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', help='called when new game')
    parser.add_argument('--iterations', help='number of iterations in game')
    parser.add_argument('--last_opponent_move', help='last opponent move')
    args = parser.parse_args()

    isNewGame = args.init
    countIterations = args.iterations
    moveOpPrevious = args.last_opponent_move

    #if isNewGame:
        #generate json
    #cooperate first x3, see how they go
    #3 coop sucker
            #wait for 1 strikes
    #2 coop sneaky
            #wait for 3 strikes
    #1 coop tricky
            #tit for tat
    #0 coop beligerant
            #do not forgive
    #for each snitch, add to linked list


    #for the next x turns, do not cooperate, afterwards, forgive coop for 2 to see if they are back to normal
    #time to judge
    #read previous history and linked list
    #after 60 turns, if snitch rate has 80% bias, snitch for the rest
        #dupe last 40 opmoves, run tests to see which will get me least time
            #if copy me or high coop, coop until they betray or go on betray streak for rand# < 5
            #if pattern detected (every 10 moves bias is similar), tit for tat
if __name__ == '__main__':
    main()

