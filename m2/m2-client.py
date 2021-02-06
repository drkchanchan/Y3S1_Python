#!/usr/bin/python3

 #==============================================================================
 #   Assignment:  Milestone 2, lottery ticket generator client
 #
 #       Author:  Derek Chan
 #     Language:  Python
 #                      
 #   To Compile:  
 #
 #        Class:   Python for Programmers: Sockets and Security DPI912
 #    Professor:  Harvey Kaduri
 #     Due Date:  2020-10-08
 #    Submitted:  2020-10-31
 #
 #-----------------------------------------------------------------------------
 #
 #    Description: Develop a client that takes arguments for number of clients to run, ip, and host.
 #        Input is taken within the script from the user for file name to store the ticket data, 
 #        the client will then generate unique ticket types and ticket amounts for each fork
 #        and send that to the daemon, ticket data is sent back to the client, client will
 #        format and write the data into each file for each child process there is.
 #
 #    Collaboration:  
 #
 #    Input: User will provide an amount of client processes to be created from the CLI, port and IP is 
 #        also in the CLI. User input will be requested in the script for the name of the file for tickets to be
 #        written into
 #
 #    Output:  Ticket data is outputted into unique files depending on the number of processes requested.
 #        A print line is also provided to for each ticket file that has been generated.
 #
 #    Algorithm:  The client prompts the user for a file name to write to. Client will then generate number of
 #        processes based on CLI argument. Each forked process will be provided a random ticket type and a
 #        random amount of tickets to be generated. Client forked processes receive the ticket Data back and
 #        formats and writes the ticket data into the corresponding folder
 #
 #    Required Features Not Included:  
 #
 #    Known Bugs:  None that I can find
 #
 #    Classification: Will be attempting prototype A
 #
#==============================================================================

import argparse
import os
import socket
import sys
import random

from socket import *

#defining the processHandler Function
#focuses on forking and providing the randomly generated ticket type and ticket amount
#forked processes establish, send and receive data in this function as well
def processHandler(processAmount, daemonIP, daemonPort):
    fileCount = 1
            
    fileName = input('Please enter new ticket file name: ')
    
    #for loop to create the number of forks specified by the user 
    for currentProcess in range(processAmount):
        
        #each child process is provided the file name and a count, this way each child process is
        #provided its own unique file name
        tempFileName = f'{fileName}{fileCount}'
        fileCount += 1
        try:
            pid = os.fork()
        except OSError:
            sys.stderr.write('Failed to create child process')
            continue
        
        #if process is a child process, randomly generate details for ticket type and amoun.
        #data is sent to daemon to be processed and results will be returned
        #results are decoded and passed to fileHandler function
        if (pid == 0):
            numberOfTickets = random.randrange(1, 4)
            typeOfTicket = ticketType[random.randrange(3)]
            toServer = f'{typeOfTicket} {numberOfTickets}'
            socketConnection = socket(AF_INET6,  SOCK_STREAM)
            socketConnection.connect((daemonIP,  daemonPort))
            socketConnection.send(toServer.encode('utf-8'))
            receivedData = socketConnection.recv(128 * maxTicketAmount)
            receivedData = receivedData.decode('utf-8')
            fileHandler(receivedData, typeOfTicket, numberOfTickets, tempFileName)
            os._exit(0)

# defining the fileHandler Function
# focuses on changing the string of data back into lists, writes to file after
def fileHandler(ticketData, ticketType, ticketAmount, fileName):
    ticketList = []

    if(ticketType == '649' or ticketType == 'dg'):
        ticketList = ticketData.split('\n')
        ticketList = ['[' + item + ']' for item in ticketList]

    elif(ticketType == 'max'):
        ticketList = ticketData.split('\n')
        for i in range(0, ticketAmount):
                setData = ticketList[i].split('/')
                setData = ['[' + item + ']' for item in setData]
                ticketList[i] = setData

    openedFile = open(fileName,  "w")
    if(ticketType == '649'):
        for i in range(0, ticketAmount):
            openedFile.write(f"lotto649 ticket #{i + 1} {ticketList[i]}\n")

    elif(ticketType == 'max'):
        for i in range(0, ticketAmount):
            openedFile.write(f"lottoMax ticket #{i + 1}\n")
            for j in range(len(ticketList[i])):
                openedFile.write(f"set# {j + 1} {ticketList[i][j]}\n")

    elif(ticketType == 'dg'):
        for i in range(0, ticketAmount):
            openedFile.write(f"lotto Daily Grand ticket #{i + 1} {ticketList[i]}\n")
    openedFile.close()
    print(f'Ticket Data was saved in {fileName}.\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Milestone 2: Lottery ticket generator client')

    parser.add_argument('-c', type = int, default = 3, required = True, dest = 'processAmount', 
        help = 'The number of processes to be generated, MAX IS 10, DEFAULT is 3')

    parser.add_argument('-ip',  action = 'store_const', dest = 'ip',
        const = '::1', required = True, help = 'Using IP ...')

    parser.add_argument('-port', action = 'store_const', dest = 'port',
        const = 8080, required = True,
        help = 'Using Port 8080 for ticket generator daemon')

    parameters = parser.parse_args()
    
    random.seed()
    maxProcessAmount = 10
    maxTicketAmount = 4
    fileName = ''
    tempFileName = ''
    ticketType = ['649',  'max',  'dg']
    
    #check if the amount provided is safe, if not, set to default amount
    if (parameters.processAmount < 1 or parameters.processAmount > maxProcessAmount):
        print(f'The amount entered is more than the max or less than 1, setting amount to 3 processes')
        parameters.processAmount = 3
    
    processHandler(parameters.processAmount,  parameters.ip, parameters.port)
    
    childCount = 0
    while (childCount < parameters.processAmount):
        os.waitpid(0, 0)
        childCount += 1
    sys.exit()
