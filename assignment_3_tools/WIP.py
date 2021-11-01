# -*- coding: utf-8 -*-
'''
Created on Sun Oct 31 07:03:27 2021

@author: Michael Nguyen 200860392
'''
import argparse
import random
import json

HISTORY_FILE = 'history.json'
DATASTRUCT_FILE = 'data.json'
TURNING_POINT = 60  # nth iteration to begin advanced algo


def jsonDump(file, dictData):  # obj to json file
    with open(file, 'w') as writeFile:
        json.dump(dictData, writeFile)


def jsonLoad(file):  # json file to obj
    with open(file, 'r') as readFile:
        return json.load(readFile)


"""
# either im stupid or this is no function to return and remove first obj in a list in a dict
def dictQueuePop(dictData):
    qPop = dictData['queue'][0]
    del dictData['queue'][0]
    return qPop
"""  # I am stupid


def compareHist(histMe, histOp):
    score = 0
    for i in len(histOp):
        if histMe[i] == 'confess' and histOp[i] == 'silent':
            score += 1  # ftw
        elif histMe[i] == 'silent' and histOp[i] == 'confess':
            score -= 1  # epic fail
    return score


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

    if isNewGame:  # generate fresh json file
        #dict templates
        dictHistory = {
            'personality': -1,
            'history': []
        }
        dictData = {
            'queue': ['silent', 'silent', 'silent'],
            'currIteration': 0,
        }
        jsonDump(HISTORY_FILE, dictHistory)
        jsonDump(DATASTRUCT_FILE, dictData)
    else:  # time to load jsons
        dictHistory = jsonLoad(HISTORY_FILE)
        dictData = jsonLoad(DATASTRUCT_FILE)
        # update opponent history
        dictHistory['history'].append(moveOpPrevious)
        dictData['currIteration'] += 1  # update current iteration
        jsonDump(HISTORY_FILE, dictHistory)
        jsonDump(DATASTRUCT_FILE, dictData)

    #First 3 moves shall be to remain silent, see what oponent does and assign personality accordingly
    # opponent algo personality is unknown
    if dictHistory['personality'] == -1 and bool(dictData['queue']):
        print(dictData['queue'].pop(0))  # FIFO
    elif dictHistory['personality'] == -1:  # First 3 moves are dealt, time to judge
        # Based on number of silent in opponent's first 3 moves: 3:nice 2:sneaky 1:tricky 0:belligerent
        dictHistory['personality'] = dictHistory['history'].count('silent')

    # Opponent may switch algo after around the nth iteration mark, for now simple algo will suffice
    if dictHistory['personality'] > -1 and dictData['currIteration'] <= TURNING_POINT:
        # 3/4 the time confess unless opponent confessed as last move
        if dictHistory['personality'] == 3:  # personality nice
            if moveOpPrevious != 'confess':  # the opponent be a trustin' one
                rng = random.randrange(4)  # furl the die
                if rng != 0:  # bad luck t' me opponent
                    print('confess')  # we do a wee trollin'
                else:  # luck be on thar side
                    print('silent')  # good fer 'em
            else:  # i 'ave learned me lesson, fer now
                print('silent')  # i swear on me beard

        # silent until opponent confesses, retaliate then forgive after 2 confess
        elif dictHistory['personality'] == 2:  # personality sneaky
            if bool(dictData['queue']):  # empty queue of confessions
                print(dictData['queue'].pop(0))  # sins are forgiven
            elif moveOpPrevious == 'confess':  # retaliate for their transgression
                print('confess')  # one as penence
                dictData['queue'].append('confess')  # another as penence
            else:  # absolution
                print('silent')

        # silent until opponent confesses, then retaliate until silent
        elif dictHistory['personality'] == 1:  # personality tricky
            if moveOpPrevious == 'confess':  # teach 'em a lesson
                print('confess')  # that'l teach 'em
            else:  # quiet neighbors make for good neighbors
                print('silent')  # work with me here

        # silent until opponent confesses, never forgive never forget
        elif dictHistory['personality'] == 0:  # personality belligerent
            if dictHistory['history'].count('confess') <= 3:
                # we remaineth in tenuous standings
                print('silent')  # i shalt coop'rate f'r anon
            else:  # the opponent hast wrong'd me
                # i shalt nev'r f'rgive this slight 'gainst me
                print('confess')

    # judgement day has come
    elif dictHistory['personality'] > -1 and dictData['currIteration'] > TURNING_POINT:
        numSilent = dictHistory['history'].count('silent')
        numConfess = dictHistory['history'].count('confess')
        trustFactor = numSilent/dictData['currIteration']
        distrustFactor = numConfess/dictData['currIteration']

        if distrustFactor >= .80:  # opponent cannot be trusted
            print('confess')  # i will not play their game

        else:  # advanced value based algos
            #history repeats itself/poor man's machine learning
            predictiveHist = dictHistory['history'].append(
                dictHistory['history'][3:])  # basically duplicate the history
            if len(predictiveHist) > numIterations:  # trim it to iteration length
                del predictiveHist[:-
                                   (dictData['currIteration']*2-numIterations)]

            # to determine winner of value based algo
            dictValue = {1: 0, 2: 0, 3: 0, 4: 0}
            #its late and i am going crazy so i will comment less, good luck
            #initialize move histories based on probability
            probHist1 = []
            probHist2 = []
            probHist3 = []
            probHist4 = []
            for i in range(100):
                if random.range(numSilent) == 0:  # 1/numSilent chance its silent
                    probHist1.append("silent")
                else:
                    probHist1.append("confess")

                if random.range(numSilent) != 0:  # 1/numSilent chance its confess
                    probHist2.append("silent")
                else:
                    probHist2.append("confess")

                if random.range(numConfess) == 0:  # 1/numConfess chance its silent
                    probHist3.append("silent")
                else:
                    probHist3.append("confess")

                if random.range(numConfess) != 0:  # 1/numConfess chance its confess
                    probHist4.append("silent")
                else:
                    probHist4.append("confess")

            #compare and see which one comes on top
            dictValue[1] = compareHist(probHist1, predictiveHist)
            dictValue[2] = compareHist(probHist2, predictiveHist)
            dictValue[3] = compareHist(probHist3, predictiveHist)
            dictValue[4] = compareHist(probHist4, predictiveHist)
            winner = max(dictValue, key=dictValue.get)  # get winner
            #use winner's prediction
            if winner == 1:
                print(probHist1[dictData['currIteration']])
            elif winner == 2:
                print(probHist2[dictData['currIteration']])
            elif winner == 3:
                print(probHist3[dictData['currIteration']])
            elif winner == 4:
                print(probHist4[dictData['currIteration']])

    jsonDump(HISTORY_FILE, dictHistory)
    jsonDump(DATASTRUCT_FILE, dictData)


if __name__ == '__main__':
    main()
