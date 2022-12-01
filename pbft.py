#
#  PBFT Algorithm for CS 4371
#  Coded by: Jonathan Sibbett
#
import hashlib
import random

from block import *

# Forms a blockchain of length n
def makeBlockchain(numNodes):
    i = 0
    list = []
    previous = ""
    while(i < numNodes):
        key = str(i)
        list.append(block(key, "Some Data"))
        if(i > 0):
            list[i].set_previous(previous)
        previous = list[i].get_hash()
        i = i+1

    return list

# introduces N number of traitorous nodes into a blockchain
def makeTraitor(blockchain, numTraitors, length):
    randomList = []
    for i in range(numTraitors):
        newNum = False
        # generates a new number everytime
        while (newNum == False):
            r = random.randint(0, length-1)
            if r not in randomList:
                randomList.append(r)
                newNum = True
        blockchain[r].set_valid(False)

def printResult(data, traitors, nodes):
    print("-----------------")
    print("\nNumber of nodes: {}".format(nodes))
    print("Number of Traitors: {}".format(traitors))
    print("Result: {}".format(data))
    print("\n-----------------\n")
    


def pbft(primary, tolerance, length, request):
    # send a preprepare message to all nodes in the chain
    for i in range(length):
        if(i != request and primary[request-1].get_valid() == True):
            primary[i].send_request(0)

    # Send a prepare message if the node is valid
    for i in range(length):
        if(primary[i].get_valid() == True and primary[i].get_preprepare() == 1):
            # If the node is valid send a prepare message to all other nodes
            for j in range(length):
                primary[j].send_request(1)
    
    # Check for at least 1/3 of nodes have returned the prepare message
    for i in range(length):
        if(primary[i].get_valid() == True and primary[i].get_prepare() >= (2*tolerance)):
            # If the checks pass send a commit message to all nodes in the chain
            for j in range(length):
                primary[j].send_request(2)

    # Check for at least 1/3 of the nodes returned a commit message
    replyCount = 0
    for i in range(length):
        if(primary[i].get_valid() == True and primary[i].get_commit() >= (2*tolerance+1)):
            # If the check pass send a reply to client
            replyCount += 1

    # If the reply count is lower then the tolerance then return the data at that node
    if(replyCount >= (2*tolerance+1) and replyCount != 0):
        return primary[request].get_data()
    else: 
        return "PBFT Check failed"

#Block tests with 3 traitors and 10 nodes
tolerance = 3
nodes = 3 * tolerance + 1
traitors = 5

blockChain = makeBlockchain(nodes)

makeTraitor(blockChain, tolerance, nodes)
givenData = pbft(blockChain, tolerance, nodes, random.randint(1,nodes))

printResult(givenData, tolerance, nodes)

# Test with 5 traitors and 10 nodes
tolerance = 3
blockChain = makeBlockchain(nodes)
traitors = 5
makeTraitor(blockChain, traitors, nodes)
givenData = pbft(blockChain, tolerance, nodes, random.randint(1,nodes))

printResult(givenData, traitors, nodes)
# Test with between 1 and 50 traitors and between 100 and 200 nodes
traitors = random.randint(32, 67)
nodes = random.randint(100,200)
blockChain = makeBlockchain(nodes)
tolerance = int(nodes / 3)

makeTraitor(blockChain, traitors, nodes)
givenData = pbft(blockChain, tolerance, nodes, random.randint(1,nodes))

printResult(givenData, traitors, nodes)