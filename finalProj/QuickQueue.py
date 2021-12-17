#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:51:10 2021

The QuickQueue system is inspired by but is legally distinct from the DisneyTM FastPassTM system.
The creator of this program does not intend to infringe on any copywrite or intellectual property

@author: Michael Nguyen 200860392
"""
import random


class InsertSortRide:  # insertion sort algo ride
    def __init__(self):
        self.curRider = None  # current rider being sorted
        self.waitTime = 0  # how long it will take to sort
        self.listSorted = []  # sorted riders

    def sortRider(self, rider):  # accept rider to ride and sort
        print(str(rider.value) + " has entered the ride")
        if not self.listSorted:  # if list is empty, add first rider
            self.listSorted.append(rider)
        else:  # insertion sort algo
            for i, val in enumerate(self.listSorted):  # traverse sorted list
                if rider.value < val.value:  # if rider value is lower than current element
                    # insert right before current element
                    self.listSorted.insert(i, rider)
                    break  # done sorting
                # reached end of list, larger than all elements
                elif i == len(self.listSorted)-1:
                    self.listSorted.append(rider)
                    break  # done sorting, also done to prevent duplication
        # wait time is essentially length of list
        self.waitTime = len(self.listSorted)
        return self.waitTime  # return wait time as cooldown time

    def print(self):  # print sorted list
        printList("Sorted List", self.listSorted)


class ParkGuest:
    def __init__(self, value):

        self.value = value        # Guest's value to be sorted
        self.timeWaited = 0  # time spent waiting in a queue
        self.quickTicketTime = None  # time they should return with thie QuickTicket

    def wait(self):  # increment time spend waiting
        self.timeWaited += 1


class Queue:  # FIFO stack
    def __init__(self):
        self.list = []
        self.length = 0

    def push(self, guest):  # Guest enters queue
        self.list.append(guest)
        self.length += 1  # increment queue length

    def pop(self):  # guest leaves queue
        if self.list:
            self.length -= 1  # decrement queue length
            return self.list.pop(0)

    def print(self, event):  # print queue
        print(event + ':')  # print queue event
        print('<-[', end='')  # print front of queue
        for i, val in enumerate(self.list):
            if i != (self.length-1):  # avoid printing empty space at end
                print(str(val.value) + ", ", end='')
            else:
                print(str(val.value), end='')
        print(']<-')  # print back of queue

    def updateWait(self):  # update all wait times for guests in queue
        for guest in self.list:
            guest.wait()

    def isEmpty(self):
        if self.list:
            return False
        else:
            return True


# print list made as its own function because i use it like two times and its slightly different from printing a queue
def printList(event, listToPrint):
    print(event + ':')  # print list event
    print('[', end='')
    for i, val in enumerate(listToPrint):
        if i != (len(listToPrint)-1):  # avoid printing empty space at end
            print(str(val.value) + ", ", end='')
        else:
            print(str(val.value), end='')
    print(']')


def main():
    
    tick = 0  # clock
    avrgTick = 0  # current average ride wait time

    numGuest = 25  # number of guests

    parkGuests = []  # guests in park
    normalQueue = Queue()  # guests in normal queue for insertion sort ride
    quickQueue = Queue()  # guests in quick queue for insertion sort ride
    ride = InsertSortRide()  # insert sort ride

    for i in range(numGuest):  # generate sorting park guests
        parkGuests.append(ParkGuest(random.randrange(numGuest)))
    printList("Initial Park Guests", parkGuests)
    originalParkGuests = parkGuests.copy()  # original unsorted list for posterity

    # run QuickQueue sim, continue until list is fully sorted
    while len(ride.listSorted) < numGuest:
        print("Tick: " + str(tick))  # print clock

        if parkGuests:  # guests attempt to enter queue if there are park guests available
            guest = random.choice(parkGuests)  # pick a random park guest
            if guest.quickTicketTime is None:  # prevent guests with QuickTicket from entering normal queue or redrawing QuickTicket
                if random.choice([0, 1]):  # 50% probabilitiy of being in normal queue
                    print(str(guest.value) + " enters the Normal Queue")
                    normalQueue.push(guest)
                    parkGuests.remove(guest)
                else:  # guest gets QuickTicket
                    # have QuickTicket guest enter quick queue [avrgTick] from current time
                    quickWaitTime = tick + avrgTick
                    print(
                        str(guest.value) + "'s QuickTicket says to return at " + str(quickWaitTime))
                    guest.quickTicketTime = quickWaitTime
            # this nested for loop may be bad and i am sorry but my final project proved to be more complex than I had planned and I am limited by my knowledge of python
            for quickGuest in parkGuests:  # see if any guest is ready to return at their QuickQueue time
                if quickGuest.quickTicketTime == tick:
                    quickQueue.push(quickGuest)
                    parkGuests.remove(quickGuest)
                    print(str(quickGuest.value) +
                          " enters the Quick Queue")
                    break
        # guests in queue must wait for ride to be not busy
        if ride.waitTime == 0:  # ride is free to accept a rider
            if not quickQueue.isEmpty():  # prioritise quick queue guests
                avrgTick = ride.sortRider(quickQueue.pop())
            elif not normalQueue.isEmpty():  # let normal queue guests ride
                avrgTick = ride.sortRider(normalQueue.pop())
            tick += 1  # increment clock
        else:  # ride is busy
            ride.waitTime -= 1  # decrement ride wait time
            tick += 1
            # update wait time of guests in queues
            normalQueue.updateWait()
            quickQueue.updateWait()
        printList("Park Guests", parkGuests)
        normalQueue.print("Normal Queue")
        quickQueue.print("Quick Queue")
        print("Time left until a guest can ride: " + str(ride.waitTime))
        ride.print()
        print('')
    # calculate average overall wait time
    printList("Original Unsorted List", originalParkGuests)
    print('\n'+"Number of Guests: " + str(numGuest))
    sumAll = 0
    for rider in ride.listSorted:  # calculate overal queue wait time
        sumAll += rider.timeWaited
    print("Overall Average Wait Time: " +
          str(round(sumAll/numGuest, 2)) + " Ticks")
    sumNorm = 0
    numNorm = 0
    sumQuick = 0
    numQuick = 0
    for rider in ride.listSorted:
        if rider.quickTicketTime is None:  # calculate average normal queue wait time
            numNorm += 1
            sumNorm += rider.timeWaited
        else:  # calculate average quick queue wait time
            numQuick += 1
            sumQuick = + rider.timeWaited
    print("Normal Queue Average Wait Time: " +
          str(round(sumNorm/numNorm, 2)) + " Ticks")
    print("Quick Queue Average Wait Time: " +
          str(round(sumQuick/numQuick, 2)) + " Ticks")


if __name__ == '__main__':
    main()
