#
#  PBFT Algorithm for CS 4371
#  Coded by: Jonathan Sibbett
#
import hashlib
import random

class block:
    def __init__(self, key,):
        self.previous_node = "NONE"
        self.node_hash = hashlib.sha256(key.encode()).hexdigest() & 0xf
        self.node_preprepare = 0
        self.node_prepare = 0
        self.node_commit = 0
        self.data = ""
    
    def set_previous(previousHash):
        self.previous_node = previousHash

    def get_previous():
        return self.previous_node

    def get_hash():
        return self.node_hash

    def get_preprepare(previousHash):
        return self.node_preprepare
    
    def get_prepare(previousHash):
        return self.node_prepare

    def get_commit(previousHash):
        return self.node_commit


    def send_request(reqType):
        if (reqType == 1):
            self.node_prepare += 1
        elif(reqType == 2):
            self.node_commit += 1
        elif(reqType == 0):
            self.node_preprepare += 1
            

    def set_data(strdata):
        self.data = strdata


# Forms a blockchain of length n
def makeBlockchain(numNodes):
    i = 0
    list = []
    previous = 0
    while(i < numNodes):
        key = str(i)
        list.append(block(key))
        if(i > 0):
            list[i].set_previous(previous)
        previous = list[i].get_hash()
        i = i+1

    return list

# introduces N number of traitorous nodes into a blockchain
def makeTraitor(blockchain, numTraitors, length):
    randomList = []
    for i in numTraitors:
        newNum = False
        # generates a new nu
        while (newNum == False):
            r = random.raident(1, length)
            if r not in randomList:
                randomList.append(r)
                nuwNum = True
        blockchain[r].set_previous = "NONE"


def pbft(primary, rep2, rep3, rep4, tolerance, request):
    # send a preprepare message and collect the previous hash
    previousNode = primary[request].get_previous
    rep2[request].send_request(0)
    rep3[request].send_request(0)
    rep4[request].send_request(0)

    # Send a prepare Message if they previous Hash matches the primary node
    if (rep2[request].get_preprepare() == 1 and rep2[request].get_previous() == previousNode):
        primary[request].send_request(1)
        rep2[request].send_request(1)
        rep3[request].send_request(1)
        rep4[request].send_request(1)
    if (rep3[request].get_preprepare() == 1 and rep3[request].get_previous() == previousNode):
        primary[request].send_request(1)
        rep2[request].send_request(1)
        rep3[request].send_request(1)
        rep4[request].send_request(1)
    if (rep4[request].get_preprepare() == 1 and rep4[request].get_previous() == previousNode):
        primary[request].send_request(1)
        rep2[request].send_request(1)
        rep3[request].send_request(1)
        rep4[request].send_request(1)
    
    # Check for at least 1/3 of reps have returned the prepare message and if so return a commit message
    if (primary[request].get_previous() == previousNode and tolerance >= primary[request].get_prepare):
        primary[request].send_request(2)
        rep2[request].send_request(2)
        rep3[request].send_request(2)
        rep4[request].send_request(2)
    if (rep2[request].get_previous() == previousNode and tolerance >= rep2[request].get_prepare):
        primary[request].send_request(2)
        rep2[request].send_request(2)
        rep3[request].send_request(2)
        rep4[request].send_request(2)
    if (rep3[request].get_previous() == previousNode and tolerance >= rep3[request].get_prepare):
        primary[request].send_request(2)
        rep2[request].send_request(2)
        rep3[request].send_request(2)
        rep4[request].send_request(2)
    if (rep4[request].get_previous() == previousNode and tolerance >= rep4[request].get_prepare):
        primary[request].send_request(2)
        rep2[request].send_request(2)
        rep3[request].send_request(2)
        rep4[request].send_request(2)

    # Check for the number of commits on it, if it is greater then the tolerance send a reply to the client
    replyCount = 0
    if(primary[request].get_commit() <= tolerance):
        replyCount += 1
    if(rep2[request].get_commit() <= tolerance):
        replyCount += 1
    if(rep3[request].get_commit() <= tolerance):
        replyCount += 1
    if(rep4[request].get_commit() <= tolerance):
        replyCount += 1

    # Return the total number of replys to the client    
    return replyCount

tolerance = 3
nodes = 3 * tolerance + 1

primary = makeBlockchain(nodes)
rep2, rep3, rep4 = primary

makeTraitor(rep2, nodes, nodes)
pbft(primary, rep2, rep3, rep4, tolerance, 4)

