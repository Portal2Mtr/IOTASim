import random
from bundle import Bundle
# Manages the tangle in its entirety, several tangle Nodes and many bundles.
class Tangle:
    def __init__(self):

        # One trxn with a bundle to start as genesis, random selection with replacement allows for growing tangle
        # ==> URTS
        # TGraph key {key: [trnxObject]}
        self.genBundle = Bundle(None,None, None) # Setup genesis Bundle
        self.genBundle.addTrxn(self.genBundle)

        self.tGraph = {'genesis_trxn': [None]}
        self.bundleObjects = {'genesis_trxn': self.genBundle}

        # No data to start
        self.tData = {}

        # Five nodes for example
        self.tLedger = {}
        self.netNodes = []

    # Initialize the ledger with a balance for each virtual node.
    def initLedger(self,node):
        self.tLedger[node.name] = node.bal
        self.netNodes.append(node)

    # Add a bundle with a trxn to the tangle and verify with PoW
    def add_tx(self,bundle: Bundle):
        if bundle.branch in self.tGraph and bundle.trunk in self.tGraph:
            # TODO: Add realistic support for value transactions
            if bundle.trxns[0].value_tx:
                if self.check_value_tx(bundle.value_tx):
                    self.move_money(bundle.value_tx['senderID'],
                               bundle.value_tx['receiverID'],
                               bundle.value_tx['amount'])
                    self.tGraph[bundle.get_hash()] = [bundle.branch, bundle.trunk]
                    self.tData[bundle.get_hash()] = {'data_payload': bundle.data_payload,
                                                     'value_payload': bundle.value_tx}
            else:
                logHash = bundle.get_hash()
                self.tGraph[logHash] = [bundle.branch, bundle.trunk]
                self.tData[logHash] = bundle.data_payload
                self.bundleObjects[logHash] = bundle

    # Get tips from tangle randomly (normally MCMC in old IOTA, modified URTS in new IOTA)
    def find_tips(self):
        # Uses URTS algorithm for selecting tips with replacement. Results in lazy tips.
        tipChoices = list(set(self.tGraph.keys()))
        return tuple(random.choices(tipChoices, k=2))

    # Check if sender has the appropriate amount of crypto to send.
    def check_value_tx(self,value_tx):
        if value_tx['sender'] in self.tLedger:
            if value_tx['amount'] <= self.tLedger[value_tx['sender']]:
                # if signature is valid too
                res = True
        return res

    # Moves crypto from a sender to a receiver account
    def move_money(self,sender, receiver, amount):
        self.tLedger[sender.name] -= amount
        sender.bal -= amount
        if receiver.name in self.tLedger:
            self.tLedger[receiver.name] += amount
            receiver.bal += amount
        else:
            self.tLedger[receiver.name] = amount
            receiver.bal += amount