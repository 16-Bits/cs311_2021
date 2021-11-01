# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 07:03:27 2021

@author: Michael Nguyen 200860392
"""
import argparse
import random
import json

HISTORY_FILE = 'history.json'
DATASTRUCT_FILE = 'data.json'
TURNING_POINT = 60  # nth iteration to begin advanced algo


def main():

    #arguement parameter parsing to get game info
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', help='called when new game')
    parser.add_argument('--iterations', help='number of iterations in game')
    parser.add_argument('--last_opponent_move', help='last opponent move')
    args = parser.parse_args()
    #save arguement values locally
    isNewGame = args.init
    numIterations = args.iterations
    moveOpPrevious = args.last_opponent_move

    #dict templates
    dictHistory = {
        "personality": -1,
        "history": []
    }
    dictData = {
        "queue": ["silent", "silent", "silent"],
        "currIteration": 0
    }

    if isNewGame:  # generate fresh json file
        with open(HISTORY_FILE, "w") as writeFile:
            json.dump(dictHistory, writeFile)
        with open(DATASTRUCT_FILE, "w") as writeFile:
            json.dump(dictData, writeFile)
    else:  # time to load jsons
        with open(HISTORY_FILE, "r") as readFile:
            dictHistory = json.load(readFile)
            # update opponent history
            dictHistory['history'].append(moveOpPrevious)
        with open(DATASTRUCT_FILE, "r") as readFile:
            dictData = json.load(readFile)
            dictData['currIteration'] += 1  # update current iteration

    #First 3 moves shall be to remain silent, see what oponent does and assign personality accordingly
    # opponent algo personality is unknown
    if dictHistory['personality'] == -1 and not dictData['queue'].empty():
        print(dictData['queue'].pop(0))  # FIFO
    elif dictHistory['personality'] == -1:  # First 3 moves are dealt, time to judge
        # Based on number of silence in opponent's first 3 moves: 3:nice 2:sneaky 1:tricky 0:belligerent
        dictHistory['personality'] = dictHistory['history'].count('silence')

    #Opponent may switch algo after around the nth iteration mark, for now simple algo will suffice
    if dictData['currIteration'] <= TURNING_POINT:
        # 1/4 the time confess unless opponent confessed as last move
        if dictHistory['personality'] == 3:  # personality nice
            if moveOpPrevious != 'confess':  # the opponent be a trustin' one
                rng = random.randrange(4)  # furl the die
                if rng == 1:  # bad luck t' me opponent
                    print('confess')  # we do a wee trollin'
                else:  # luck be on thar side
                    print('silence')  # good fer 'em
            else:  # i 'ave learned me lesson, fer now
                print('silence')  # i swear on me beard

        # silent until opponent confesses, retaliate then forgive after 2 confess
        elif dictHistory['personality'] == 2:  # personality sneaky
            if not dictData['queue'].empty():  # empty queue of confessions
                print(dictData['queue'].pop(0))  # sins are forgiven
            elif moveOpPrevious == 'confess':  # retaliate for their transgression
                print('confess')  # one as penence
                dictData['queue'].push('confess')  # another as penence
            else:  # absolution
                print('silence')

        # silent until opponent confesses, then retaliate until silence
        elif dictHistory['personality'] == 1:  # personality tricky
            if moveOpPrevious == 'confess':  # teach 'em a lesson
                print('confess')  # that'l teach 'em
            else:  # quiet neighbors make for good neighbors
                print('silence')  # work with me here

        # silent until opponent confesses, never forgive never forget
        elif dictHistory['personality'] == 0:  # personality belligerent
            if dictHistory['history'].count('confess') <= 3:
                # we remaineth in tenuous standings
                print('silence')  # i shalt coop'rate f'r anon
            else:  # the opponent hast wrong'd me
                print('confess')  # i shalt nev'r f'rgive this slight 'gainst me

    else:  # judgement day has come
        numSilence = dictHistory['history'].count('silence')
        numConfess = dictHistory['history'].count('confess')
        trustFactor = numSilence/dictData['currIteration']
        distrustFactor = numConfess/dictData['currIteration']
        if trustFactor <= 20:  # opponent cannot be trusted
            print('confess')        #i will not play their game
        predictiveHist = dictHistory['history'].append(dictHistory['history'])
    #dupe last 40 opmoves, run tests to see which will get me least time
    #if copy me do opposite of thier last move?
    #high silent, silent until they betray or go on betray streak for rand# < 5
    #if pattern detected (every 10 moves bias is similar), copy last move
    #for the next x turns, do not silent, afterwards, forgive silent for 2 to see if they are back to normal


if __name__ == '__main__':
    main()
