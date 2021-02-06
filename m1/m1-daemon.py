#!/usr/bin/python3

#==============================================================================
 #   Assignment:  Milestone 1, lottery ticket generator client
 #
 #       Author:  Derek Chan
 #     Language:  Python
 #
 #   To Compile:  
 #
 #        Class:   Python for Programmers: Sockets and Security DPI912
 #    Professor:  Harvey Kaduri
 #     Due Date:  2020-10-08
 #    Submitted:  
 #
 #-----------------------------------------------------------------------------
 #
 #  Description: Develop a client that takes input from user that will then be sent to
 #      the daemon, the daemon will then generate ticket and send data back to client, client will
 #      format the data received
 #
 #  Collaboration:  
 #
 #
 #        Input:  The daemon will take data from the socket that it is receiving from the
 #     connection to the client
 #
 #       Output:  Daemon will generate the numbers for the type of ticket it is requested to
 #    do and send it back to the client
 #
 #    Algorithm:  The client will be sending data to the daemon which will then generate
 #      the numbers for the type of ticket requested and send it back to the client to be
 #      displayed to the user
 #
 #   Required Features Not Included:  
 #
 #   Known Bugs:  
 #
 #   Classification: Will be attempting prototype A
 #
#==============================================================================

import random
import socket

from socket import *


def handleRequest(socketConnection):

    lotteryPool = []
    temporaryString = ""

    ticketType = socketConnection.recv(2048)
    ticketType = ticketType.decode('utf-8')

    ticketAmount = socketConnection.recv(2048)
    ticketAmount = ticketAmount.decode('utf-8')

    if(ticketType == '649'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked

        for i in range(0, int(ticketAmount)):
            lotteryPool = list(range(1, 50))

            #numbers in the pool are shuffled each time the for loop is called
            #a number is popped from the lotteryPool list and saved into pickedNumber variable
            #the number is then appended to a temporaryTicket list
            for j in range(0, 6):
                random.shuffle(lotteryPool)
                pickedNumber = lotteryPool.pop()
                temporaryString += str(pickedNumber)
                if(j < 5):
                    temporaryString += ', '
            if(i < (int(ticketAmount)-1)):
                temporaryString += '\n'

        socketConnection.send(temporaryString.encode('utf-8'))

    elif(ticketType == 'max'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked
        for i in range(0, int(ticketAmount)):
            lotteryPool = list(range(1, 51))
            #loop to add sets of six numbers in a temporarySet list
            for j in range(0, 3):
                #numbers in the pool are shuffled each time the for loop is called
                #a number is popped from the lotteryPool list and saved into pickedNumber variable
                #the number is then appended to a temporarySet list
                for k in range(0, 7):
                    random.shuffle(lotteryPool)
                    pickedNumber = lotteryPool.pop()
                    temporaryString += str(pickedNumber)
                    if(k < 6):
                        temporaryString += ', '
                    #once a set of numbers is completed, it is added to the temporaryTicket list
                if(j < 2):
                    temporaryString += '/'
            #once all the sets of numbers are added to the temporary ticket, it is added to ticketList
            #ticketList stores all the tickets generated in a list to be displayed later
            if(i < (int(ticketAmount) - 1)):
                temporaryString += '\n'
        socketConnection.send(temporaryString.encode('utf-8'))

    elif(ticketType == 'dg'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked
        #a bonus pool list is also created for the special number from 1 to 7
        for i in range(0, int(ticketAmount)):
            lotteryPool = list(range(1, 50))
            bonusPool = list(range(1, 8))
            #numbers in the pool are shuffled each time the for loop is called
            #a number is popped from the lotteryPool list and saved into pickedNumber variable
            for j in range(0, 5):
                random.shuffle(lotteryPool)
                pickedNumber = lotteryPool.pop()
                temporaryString += str(pickedNumber)
                if(j <= 4):
                    temporaryString += ', '
            #numbers in the bonus pool are shuffled then popped as the last number for the ticket
            random.shuffle(bonusPool)
            pickedNumber = bonusPool.pop()
            temporaryString += str(pickedNumber)
            if(i < (int(ticketAmount))):
                temporaryString += '\n'
        socketConnection.send(temporaryString.encode('utf-8'))

    socketConnection.close()


def daemonLottery():

    socketListen = socket(AF_INET6, SOCK_STREAM)
    requestQueueSize = 5
    socketListen.bind(('::1', 8080))
    socketListen.listen(requestQueueSize)
    while True:
        socketConnection,  clientAddress = socketListen.accept()
        handleRequest(socketConnection)
        socketConnection.close()

if __name__ == '__main__':
    daemonLottery()
