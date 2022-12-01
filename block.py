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
        self.vaild = True
    
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

    def get_valid(self):
        return self.vaild

    def set_valid(self, state):
        self.vaild = state

    def send_request(self, reqType):
        if (reqType == 1):
            self.node_prepare += 1
        elif(reqType == 2):
            self.node_commit += 1
        elif(reqType == 0):
            self.node_preprepare =+ 1
            

    def set_data(self, strdata):
        self.data = strdata