import time
import hashlib
from collections import OrderedDict
from iota.crypto.kerl import Kerl
# from workClasses.tangle import Tangle
import sys
# from tangle import Tangle
# Block class handles management of individual transaction data on the tangle.
class Bundle:
    def __init__(self, tips,tipObjects, node):
        self.node = node # Can be None for genesis
        if tips is not None:
            (self.branch, self.trunk) = tips
            self.branchObj, self.trunkObj = tipObjects
            self.data_payload = self.node.get_random_string()
            self.bundle_hash = None
        else:
            # Genesis bundle/trxn
            self.branch = None
            self.trunk = None
            self.branchObj = None
            self.trunkObj = None
            self.data_payload = "GENESIS"
            self.bundle_hash = "GENESIS" #TODO: Change to IOTA seed?

        self.timestamp = time.time()
        self.trxns = []


    def add_value_tx(self, sender, receiver, amount):
        self.value_tx = {'sender': sender.name,
                         'receiver': receiver.name,
                         'amount': amount,
                         'signature': sender.sig,
                         'senderID' : sender,
                         'receiverID' : receiver
                         }

    def get_hash(self):
        return self.node.calc_hash(self)

    def addTrxn(self,trxnObject):
        self.trxns.append(trxnObject)
        trxnObject.idx = len(self.trxns) - 1

    def __len__(self):
        return len(self.trxns)

    def __iter__(self):
        return iter(self.trxns)




