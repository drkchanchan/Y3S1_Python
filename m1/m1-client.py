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
 #        Input:  The client will take input from the user which will be related to the 
 #     type of lottery ticket to be generating and the number of tickets to be made
 #
 #       Output:  Program will output the numbers for the type of ticket specified and
 #    and display the number of tickets that were requested
 #
 #    Algorithm:  The client will be sending data to the daemon which will then generate
 #      the numbers for the type of ticket requested and send it back to the client to be
 #      displayed to the user
 #
 #   Required Features Not Included:  
 #
 #   Known Bugs:  Having Issues with figuring why my code is erroring 
 #
 #   Classification: Will be attempting prototype A
 #
#==============================================================================

import argparse
import socket

from socket import *

parser = argparse.ArgumentParser(description='Milestone 1: Lottery ticket generator client')

lottoTypes = parser.add_mutually_exclusive_group(required=True)

lottoTypes.add_argument('-649', action='store_const', dest='lottery',
    const='649',
    help='Picks ticket type of Lotto 649 (generates 1 set of six unique numbers from 1 to 49)')

lottoTypes.add_argument('-max', action = 'store_const', dest = 'lottery',
    const = 'max',
    help = 'Picks ticket type of Lotto MAX (generates 3 sets of numbers, each taking from \
        their own pool of numbers, seven numbers from 1 to 50)')

lottoTypes.add_argument('-dg', action = 'store_const', dest = 'lottery',
    const = 'dg',
    help = 'Picks ticket type of Lotto Daily Grand (generates 1 set of 5 regular numbers from \
        1 to 49, also picks one Grand Number from a different pool from a range of 1 to 7)')

parser.add_argument('-c', type = int, required = True,  help = 'The number of tickets to be generated')

parser.add_argument('-ip',  action = 'store_const', dest = 'ip',
    const = '::1', required = True,
    help = 'Using IP ...')

parser.add_argument('-port', action = 'store_const', dest = 'port',
    const = 8080, required = True,
    help = 'Using Port 8080 for ticket generator daemon')

parameters = parser.parse_args()


def clientLottery(parameters):

    socketObject = socket(AF_INET6,  SOCK_STREAM)
    socketObject.connect((parameters.ip, parameters.port))

    encodedLotto = parameters.lottery.encode('utf-8')
    socketObject.send(encodedLotto)

    encodedNumber = str(parameters.c)
    socketObject.send(encodedNumber.encode('utf-8'))

    ticketList = []

    ticketData = socketObject.recv(2048)
    ticketData = ticketData.decode('utf-8')

    if(parameters.lottery == '649' or parameters.lottery == 'dg'):
        ticketList = ticketData.split('\n')
        ticketList = ['[' + item + ']' for item in ticketList]

    elif(parameters.lottery == 'max'):
        ticketList = ticketData.split('\n')
        for i in range(0, parameters.c):
                setData = ticketList[i].split('/')
                setData = ['[' + item + ']' for item in setData]
                ticketList[i] = setData

    fileName = input('Please enter the name of the file to be created: ')
    if(fileName):
        openedFile = open(fileName,  "w")
        if(parameters.lottery == '649'):
            for i in range(0, parameters.c):
                openedFile.write(f"lotto649 ticket #{i + 1} {ticketList[i]}\n")

        elif(parameters.lottery == 'max'):
            for i in range(0, parameters.c):
                openedFile.write(f"lottoMax ticket #{i + 1}\n")
                for j in range(len(ticketList[i])):
                    openedFile.write(f"set# {j + 1} {ticketList[i][j]}\n")

        elif(parameters.lottery == 'dg'):
            for i in range(0, parameters.c):
                openedFile.write(f"lotto Daily Grand ticket #{i + 1} {ticketList[i]}\n")
        openedFile.close()

    if(parameters.lottery == '649'):
        for i in range(0, parameters.c):
            print(f"lotto649 ticket #{i + 1} {ticketList[i]}\n")

    elif(parameters.lottery == 'max'):
        for i in range(0, parameters.c):
            print(f"\nlottoMAX ticket #{i + 1}")
            for j in range(len(ticketList[i])):
                print(f"set# {j + 1} {ticketList[i][j]}")
        print("\n")

    elif(parameters.lottery == 'dg'):
            for i in range(0, parameters.c):
                print(f"lotto Daily Grand ticket #{i + 1} {ticketList[i]}\n")
    return 0

if __name__ == '__main__':
    clientLottery(parameters)
