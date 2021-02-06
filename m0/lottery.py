#!/usr/bin/python3

#==============================================================================
 #   Assignment:  Milestone 0, lottery ticket generator
 #
 #       Author:  Derek Chan
 #     Language:  Python
 #                argparse
 #                random
 #
 #   To Compile:  n/a
 #
 #        Class:  Python for Programmers: Sockets and Security DPI912 
 #    Professor:  Harvey Kaduri
 #     Due Date:  2020-09-29 11:59AM
 #    Submitted:  2020-09-29 11:55AM
 #
 #-----------------------------------------------------------------------------
 #
 #  Description:  Develop a function that will generate lottery tickets
 #                based on the parameters passed into the function
 #
 #Collaboration:  n/a
 #
 #        Input:  The program takes in a string for the type of lottery ticket,
 #                also takes in an integer to know how many tickets to generate
 #
 #       Output:  The program will output a series of strings that will display the 
 #                tickets it has generated and the numbers for each ticket
 #
 #    Algorithm:  The program uses nested for loops and if statements to decide
 #                which ticket should be generated, how many tickets to generate,
 #                and how the numbers should be picked (to be as accurate as the
 #                actual lottery games)
 #      
 #
 #   Required Features Not Included: n/a
 #                                   
 #      
 #
 #   Known Bugs:  n/a
 #      
 #
 #   Classification: n/a
 #
#==============================================================================

import argparse
import random

parser = argparse.ArgumentParser(description='Milestone 0: Lottery ticket number generator')

lottoTypes = parser.add_mutually_exclusive_group(required = True)

lottoTypes.add_argument('-649', action = 'store_const', dest = 'lottery',
    const = '649',
    help = 'Picks ticket type of Lotto 649 (generates 1 set of six unique numbers from 1 to 49)')

lottoTypes.add_argument('-max', action = 'store_const', dest = 'lottery',
    const = 'max',
    help = 'Picks ticket type of Lotto MAX (generates 3 sets of numbers, each taking from \
        their own pool of numbers, seven numbers from 1 to 50)')

lottoTypes.add_argument('-dg', action = 'store_const', dest = 'lottery',
    const = 'dg',
    help = 'Picks ticket type of Lotto Daily Grand (generates 1 set of 5 regular numbers from \
        1 to 49, also picks one Grand Number from a different pool from a range of 1 to 7)')

parser.add_argument('-c', type = int, required = True,  help = 'The number of tickets to be generated')

parameters = parser.parse_args()

#defining the lottery ticket generation function
def lottery(parameters):
    #creating a list for tickets to be stored
    #creating a list for the pool of numbers to be stored
    ticketList = []
    lotteryPool = []
    if(parameters.lottery == '649'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked
        for i in range(0, parameters.c):
            lotteryPool = list(range(1, 50))
            temporaryTicket = []
            #numbers in the pool are shuffled each time the for loop is called
            #a number is popped from the lotteryPool list and saved into pickedNumber variable
            #the number is then appended to a temporaryTicket list
            for j in range(0, 6):
                random.shuffle(lotteryPool)
                pickedNumber = lotteryPool.pop()
                temporaryTicket.append(pickedNumber)
            #ticketList stores all the tickets generated in a list to be displayed later
            ticketList.append(temporaryTicket)
            
        for i in range(0, len(ticketList)):
            print(f"lotto649 ticket #{i + 1} {ticketList[i]}\n")

    elif(parameters.lottery == 'max'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked
        for i in range(0, parameters.c):
            lotteryPool = list(range(1, 51))
            temporaryTicket = []
            #loop to add sets of six numbers in a temporarySet list
            for j in range(0, 3):
                temporarySet = []
                #numbers in the pool are shuffled each time the for loop is called
                #a number is popped from the lotteryPool list and saved into pickedNumber variable
                #the number is then appended to a temporarySet list
                for k in range(0, 7):
                    random.shuffle(lotteryPool)
                    pickedNumber = lotteryPool.pop()
                    temporarySet.append(pickedNumber)
                #once a set of numbers is completed, it is added to the temporaryTicket list
                temporaryTicket.append(temporarySet)
            #once all the sets of numbers are added to the temporary ticket, it is added to ticketList
            #ticketList stores all the tickets generated in a list to be displayed later
            ticketList.append(temporaryTicket)
        for i in range(len(ticketList)):
            print(f"\nlottoMAX ticket #{i + 1}")
            for j in range(len(ticketList[i])):
                print(f"set# {j + 1} {ticketList[i][j]}")
        print("\n")

    elif(parameters.lottery== 'dg'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked
        #a bonus pool list is also created for the special number from 1 to 7
        for i in range(0, parameters.c):
            lotteryPool = list(range(1, 50))
            bonusPool = list(range(1, 8))
            temporaryTicket = []
            #numbers in the pool are shuffled each time the for loop is called
            #a number is popped from the lotteryPool list and saved into pickedNumber variable
            for j in range(0, 6):
                random.shuffle(lotteryPool)
                pickedNumber = lotteryPool.pop()
                temporaryTicket.append(pickedNumber)
            #numbers in the bonus pool are shuffled then popped as the last number for the ticket
            random.shuffle(bonusPool)
            pickedNumber = bonusPool.pop()
            temporaryTicket.append(pickedNumber)
            ticketList.append(temporaryTicket)
        for i in range(0, len(ticketList)):
            print(f"lotto Daily Grand ticket #{i + 1} {ticketList[i]}\n")
    return 0

lottery(parameters)
