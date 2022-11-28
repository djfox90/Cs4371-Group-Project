#
#  PBFT Algorithm for CS 4371
#  Coded by: Jonathan Sibbett
#
import hashlib
import random

class block:
    def __init__(self, key, newData):
        self.previous_node = "NONE"
        self.node_hash = hashlib.sha256(key.encode()).hexdigest()
        self.node_preprepare = 0
        self.node_prepare = 0
        self.node_commit = 0
        self.data = newData
    
    def set_previous(self, previousHash):
        self.previous_node = previousHash

    def get_previous(self):
        return self.previous_node

    def get_hash(self):
        return self.node_hash

    def get_preprepare(self):
        return self.node_preprepare
    
    def get_prepare(self):
        return self.node_prepare

    def get_commit(self):
        return self.node_commit
    
    def get_data(self):
        return self.data


    def send_request(self, reqType):
        if (reqType == 1):
            self.node_prepare += 1
        elif(reqType == 2):
            self.node_commit += 1
        elif(reqType == 0):
            self.node_preprepare =+ 1
            

    def set_data(self, strdata):
        self.data = strdata

# Forms a blockchain of length n
def makeBlockchain(numNodes):
    i = 0
    list = []
    previous = ""
    while(i <= numNodes):
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
            r = random.randint(1, length)
            if r not in randomList:
                randomList.append(r)
                newNum = True
        blockchain[r].set_previous("NONE")


def pbft(primary, rep2, rep3, rep4, tolerance, request):
    # send a preprepare message and collect the previous hash
    previousNode = primary[request].get_previous()
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
    if (primary[request].get_previous() == previousNode and tolerance-1 <= primary[request].get_prepare()):
        primary[request].send_request(2)
        rep2[request].send_request(2)
        rep3[request].send_request(2)
        rep4[request].send_request(2)
    if (rep2[request].get_previous() == previousNode and tolerance-1 <= rep2[request].get_prepare()):
        primary[request].send_request(2)
        rep2[request].send_request(2)
        rep3[request].send_request(2)
        rep4[request].send_request(2)
    if (rep3[request].get_previous() == previousNode and tolerance-1 <= rep3[request].get_prepare()):
        primary[request].send_request(2)
        rep2[request].send_request(2)
        rep3[request].send_request(2)
        rep4[request].send_request(2)
    if (rep4[request].get_previous() == previousNode and tolerance-1 <= rep4[request].get_prepare()):
        primary[request].send_request(2)
        rep2[request].send_request(2)
        rep3[request].send_request(2)
        rep4[request].send_request(2)

    # Check for the number of commits on it, if it is greater then the tolerance send a reply to the client
    replyCount = 0
    if(primary[request].get_previous() == previousNode and primary[request].get_commit() >= tolerance and primary[request].get_commit() != 0):
        replyCount += 1
    if(rep2[request].get_previous() == previousNode and rep2[request].get_commit() >= tolerance and rep2[request].get_commit() != 0):
        replyCount += 1
    if(rep3[request].get_previous() == previousNode and rep3[request].get_commit() >= tolerance and rep3[request].get_commit() != 0):
        replyCount += 1
    if(rep4[request].get_previous() == previousNode and rep4[request].get_commit() >= tolerance and rep4[request].get_commit() != 0):
        replyCount += 1

    # If the reply count is lower then the tolerance then return the data at that node
    if(replyCount >= tolerance and replyCount != 0):
        return primary[request].get_data()
    else: 
        return "PBFT Check failed"

tolerance = 3
nodes = 3 * tolerance + 1

primary = makeBlockchain(nodes)
rep2 = makeBlockchain(nodes)
rep3 = makeBlockchain(nodes)
rep4 = makeBlockchain(nodes)

#makeTraitor(rep2, nodes, nodes)
makeTraitor(rep3, nodes, nodes)
#makeTraitor(rep4, nodes, nodes)
givenData = pbft(primary, rep2, rep3, rep4, tolerance, random.randint(1,nodes))

print(givenData)
