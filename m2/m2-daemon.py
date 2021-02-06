#!/usr/bin/python3

#==============================================================================
 #   Assignment:  Milestone 2, lottery ticket generator daemon
 #
 #       Author:  Derek Chan
 #     Language:  Python
 #
 #   To Compile:  
 #
 #        Class:   Python for Programmers: Sockets and Security DPI912
 #    Professor:  Harvey Kaduri
 #     Due Date:  2020-10-27
 #    Submitted:  2020-10-31
 #
 #-----------------------------------------------------------------------------
 #
 #    Description: Develop a daemon that listens for connections, once a connection arrives,
 #        daemon will attempt to fork and the child process will then handle the client request.
 #        The child process will then receive the type of ticket to create and also how many.
 #        The generated tickets are sent back to the client as a string.
 #
 #    Collaboration:  
 #
 #    Input: The daemon will accept a connection to a client, the child process of the daemon will
 #        receive the ticket type and ticket amount.
 #
 #    Output: Daemon child process will generate the numbers for the type of ticket it is requested to
 #        do and send it back to the client as a string.
 #
 #    Algorithm:  The parent process of the daemon will constantly be listening for connections, once
 #        a connection arrives, the parent will attempt to fork and have the child process handle the request,
 #        the child process will then send the ticket data back to the client and exit.
 #
 #    Required Features Not Included:  
 #
 #    Known Bugs:  
 #
 #    Classification: Will be attempting prototype A
 #
#==============================================================================

import errno
import os
import random
import signal
import socket
import sys

from socket import *
from signal import *

#defining the function childHandler to check for zombie processes, will kill if there are any
def childHandler(signalNumber,  frame):
    while True:
        try:
            pid,  status = os.waitpid(-1,  os.WNOHANG)
        except OSError:
            return
        if pid == 0:
            return

#The requestHandler function is used by child processes so they know how to handle
#a client request, the function will receive the ticket type and amount from the client 
#and call the generateTicket Function to create the tickets. Ticket data is sent back to client
def requestHandler(socketConnection):
    clientRequest = socketConnection.recv(128)
    clientData = clientRequest.decode('utf-8')
    clientData = list(clientData.split(" "))
    ticketResults = generateTicket(clientData[0], int(clientData[1]))
    socketConnection.send(ticketResults.encode('utf-8'))
    
#This functions purpose is handling the creation of tickets.
#it will match the parameters provided to the corresponding ticket type and loop based on amount needed
def generateTicket(requestedType, requestedAmount):
    lotteryPool = []
    temporaryString = ""

    if(requestedType == '649'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked
        for i in range(0, int(requestedAmount)):
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
            if(i < (int(requestedAmount)-1)):
                temporaryString += '\n'

    elif(requestedType == 'max'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked
        for i in range(0, int(requestedAmount)):
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
            if(i < (int(requestedAmount) - 1)):
                temporaryString += '\n'

    elif(requestedType == 'dg'):
        #for loop used to generate new pool of numbers
        #and create a temporary ticket to store the numbers picked
        #a bonus pool list is also created for the special number from 1 to 7
        for i in range(0, int(requestedAmount)):
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
            if(i < (int(requestedAmount) -1)):
                temporaryString += '\n'

    return temporaryString

#The run daemon function purpose is setting up the parent process to listen for connections
#and fork itself if needed when client requests arrive
def runDaemon():
    requestQueueSize = 100
    try:
        parentSocket = socket(AF_INET6, SOCK_STREAM)
        parentSocket.setsockopt (SOL_SOCKET, SO_REUSEADDR,  1)
        parentSocket.bind(connectionData)
        parentSocket.listen(requestQueueSize)
        signal(SIGCHLD, childHandler)
        print(f'Listening on port: {daemonPort}')
        while True:
            try:
                socketConnection,  clientAddress = parentSocket.accept()
            except IOError as e:
                code, msg = e.args
                if (code == errno.EINTR):
                    continue
                else:
                    raise
            
            try:
                pid = os.fork()
            except OSError:
                sys.stderr.write('Failed to create child process')
                continue
            
            #if process is a child, it will close the parent connection and that connection will now be passed
            #to the child process instead, requestHandler function is then called to handle the request
            if (pid == 0):
                parentSocket.close()
                requestHandler(socketConnection)
                socketConnection.close()
                os._exit(0)
            else:
                socketConnection.close()
    except Exception as error:
        print(error)
        parentSocket.close()

if __name__ == '__main__':
    connectionData = ('::1',  8080)
    daemonHost = '::1'
    daemonPort = 8080
    
    runDaemon()
    sys.exit()
