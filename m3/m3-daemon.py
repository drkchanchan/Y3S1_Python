#!/usr/bin/python3

#==============================================================================
 #   Assignment:  Milestone 3, lottery ticket generator daemon
 #
 #       Author:  Derek Chan
 #     Language:  Python
 #
 #   To Compile:  
 #
 #        Class:   Python for Programmers: Sockets and Security DPI912
 #    Professor:  Harvey Kaduri
 #     Due Date:  2020-10-27
 #    Submitted:  2020-12-06
 #
 #-----------------------------------------------------------------------------
 #
 #    Description: Update the daemon so that it is able to take start/stop commands, also
 #        separate the daemon from the terminal that started the process with double fork
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
 #    Known Bugs:  Not sure how to have the -stop command delete the directory after, program will keep thinking
 #        that the process is running even though it isnt due to the directory for the daemon process still existing
 #
 #    Classification: Will be attempting prototype B, uncertain if this meets A's requirements
 #
#==============================================================================

import argparse
import atexit
import errno
import logzero
import os
import random
import signal
import socket
import sys
import time

from logzero import logger
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

#defining the function to log numbers in a file for the daemon before sending them to the user
def logNumbers(ticketNumbers):
    logger.info(f'Child: {os.getpid()} is storing generated ticket numbers: \n {ticketNumbers}')

#The requestHandler function is used by child processes so they know how to handle
#a client request, the function will receive the ticket type and amount from the client 
#and call the generateTicket Function to create the tickets. Ticket data is sent back to client
def requestHandler(socketConnection):
    clientRequest = socketConnection.recv(128)
    clientData = clientRequest.decode('utf-8')
    clientData = list(clientData.split(' '))
    ticketResults = generateTicket(clientData[0], int(clientData[1]))
    socketConnection.send(ticketResults.encode('utf-8'))
    
#This functions purpose is handling the creation of tickets.
#it will match the parameters provided to the corresponding ticket type and loop based on amount needed
def generateTicket(requestedType, requestedAmount):
    lotteryPool = []
    temporaryString = ''

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
    
    logNumbers(temporaryString)
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

#defining the function to fully daemonize and separate the program from the CLI
def daemonize(pidFile,  *, 
    stdin='/dev/null', 
    stdout='/dev/null', 
    stderr='/dev/null'):
        
        #checks to see if Daemon is already running
        if (os.path.exists(pidHolder)):
            print(pidHolder)
            logger.error('Daemon process already running.')
            raise RuntimeError('Daemon process already running.')
            
        #Attempting first fork
        try:
            if (os.fork() > 0):
                raise SystemExit(0)
        except OSError as e:
            logger.error('Failed to execute first fork for daemonize')
            raise RuntimeError('Failed to execute first fork for daemonize: ' + e)
        
        #Changing IDs of the process and permissions
        id = os.getuid()
        os.chdir('/')
        os.umask(0)
        os.setsid()
        os.setuid(id)
        os.setgid(id)
        
        #Attempting second fork
        try:
            if (os.fork() > 0):
                raise SystemExit(0)
        except OSError as e:
            logger.error('Failed to execute second fork for daemonize')
            raise RuntimeError('Failed to execute second fork for daemonize: ' + e)
            
        sys.stdout.flush()
        sys.stderr.flush()
        
        with open(stdin,  'rb',  0) as stdReplace:
            os.dup2(stdReplace.fileno(),  sys.stdin.fileno())
        with open(stdout,  'ab',  0) as stdReplace:
            os.dup2(stdReplace.fileno(),  sys.stdout.fileno())
        with open(stderr,  'ab',  0) as stdReplace:
            os.dup2(stdReplace.fileno(),  sys.stderr.fileno())
            
        dirPath = '/tmp/'
        newDirName = "tempDirectory"
        path = os.path.join(dirPath,  newDirName)

        if os.path.exists(path) == False :
            os.mkdir(path)

        with open(pidFile,  'w') as pidFile:
            print(os.getpid(),  file=pidFile)
            
        #Pid file is deleted before exiting
        atexit.register(lambda: os.remove(pidFile))
        
def sigtermHandler(signo,  frame):
    raise SystemExit(1)
    
def statusLogging():
    sys.stdout.write(f'Daemon processes given pid {os.getpid()}\n')
    
    while True:
        sys.stdout.write(f'Daemon running as of: {time.ctime()}\n')
        time.sleep(60)

if __name__ == '__main__':
    connectionData = ('::1',  8080)
    daemonHost = '::1'
    daemonPort = 8080
    pidHolder = '/tmp/tempDirectory/daemonInfo.pid'
    signal(SIGTERM,  sigtermHandler)
    
    parser = argparse.ArgumentParser(description = 'Python Milestone 3 Lottery Ticket Data Generator')
    daemonAction = parser.add_mutually_exclusive_group(required = True)
    
    daemonAction.add_argument('-start',  action = 'store_const', dest = 'daemonAction',
        help = 'starts the daemon if it is not running', 
        const = 1)
    
    daemonAction.add_argument('-stop',  action = 'store_const', dest = 'daemonAction', 
        help = 'Stops the daemon if it is running', 
        const = 0)
        
    parameters = parser.parse_args()

    logzero.logfile('/tmp/daemon-logfile.log', 
        maxBytes= 1e6,  backupCount= 2,  disableStderrLogger= True)
    
    if (parameters.daemonAction):
        try:
            daemonize(pidHolder,  stdout = '/tmp/daemon.log', 
                stderr = '/tmp/daemonErrors.log')
        except RuntimeError as e:
            print(e,  file = sys.stderr)
            raise SystemExit(1)
        logger.info(f'Started processes with {os.getpid()}')
        try:
            runDaemon()
        except Exception as e:
            logger.error(e)
            raise SystemExit(1)
            
    else:
        if os.path.exists(pidHolder):
            with open(pidHolder) as pidFile:
                os.kill(int(pidFile.read()),  SIGTERM)
        
        else:
            logger.error('Daemon is not running!')
            print('Daemon is not running!',  file = sys.stderr)
            raise SystemExit(1)






