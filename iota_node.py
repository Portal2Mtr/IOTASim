import random
import string
import hashlib

# Represents physical network node and hashing power
class IOTANode:
    def __init__(self,name,sig,initBal=100,powDelay=10):
        self.workDelay = powDelay # TODO: PoW delay?
        self.name = name
        self.sig = sig
        self.bal = initBal

    # Node gets data (ex: iot node gets data from sensor), will work for now in simulation
    def get_random_string(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

    # Calculate hash from block metadata
    def calc_hash(self,msg):
        hasher = hashlib.sha1(msg.encode()) # TODO: replace with real-world hash func?
        return hasher.hexdigest()

    def __str__(self):
        return self.name+self.sig