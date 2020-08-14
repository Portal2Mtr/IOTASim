import time
from trxn import Trxn
# Bundle class handles management of individual transaction data on the tangle.
class Bundle:

    def __init__(self, tips,tipObjects, node):
        self.node = node # Can be None for genesis
        # Check if genesis bundle
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
            self.bundle_hash = "GENESIS" # Fine for IOTA, transaction hash representation needs to be shorter that
                                         # 81 Trytes.

        self.timestamp = time.time()
        self.trxns = []
        self.tail_transaction = None

    def add_value_tx(self, sender, receiver, amount):
        # Generate two transactions, input w/ sig and output
        self.inputTrxn = Trxn(self, -amount,isValue=True)
        self.inputTrxn.senderAddr = sender.address
        self.outputTrxn = Trxn(self,amount,isValue=False)
        self.outputTrxn.recAddr = receiver.address
        self.outputTrxn.recName = receiver.name
        self.addTrxn(self.inputTrxn)
        self.addTrxn(self.outputTrxn)

    def get_hash(self):
        # Returns the tail transaction hash from the PoW done by the bundle's node.
        return self.node.calc_hash(self)

    def addTrxn(self,trxnObject):
        # Adds a trxn to the trxns list and handles indexing for trxn.
        self.trxns.append(trxnObject)
        trxnObject.idx = len(self.trxns) - 1
        if trxnObject.idx == 0:
            self.tail_transaction = trxnObject

    def __len__(self):
        return len(self.trxns)

    def __iter__(self):
        return iter(self.trxns)






