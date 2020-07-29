import time
import hashlib
from collections import OrderedDict
# from workClasses.tangle import Tangle
import sys
# from tangle import Tangle
# Block class handles management of individual transaction data on the tangle.
class Block:
    def __init__(self, tips, node):
        (self.branch, self.trunk) = tips
        self.timestamp = time.time()
        self.node = node
        self.data_payload = self.node.get_random_string()
        self.value_tx = None


    def add_value_tx(self, sender, receiver, amount):
        self.value_tx = {'sender': sender.name,
                         'receiver': receiver.name,
                         'amount': amount,
                         'signature': sender.sig,
                         'senderID' : sender,
                         'receiverID' : receiver
                         }

    def get_hash(self):
        return self.node.calc_hash(str(OrderedDict(self.__dict__)))




