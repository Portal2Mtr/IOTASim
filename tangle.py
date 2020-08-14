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
        self.tValues = {}

    # Initialize the ledger with a balance for each virtual node.
    def initLedger(self,node):
        self.tLedger[node.address] = node.bal
        self.netNodes.append(node)

    # Add a bundle with a trxn to the tangle and verify with PoW
    def add_tx(self,bundle: Bundle):
        if bundle.branch in self.tGraph and bundle.trunk in self.tGraph:
            if bundle.trxns[0].value != 0:
                if self.check_value_tx(bundle):
                    self.move_money(bundle)
                    logHash = bundle.get_hash()
                    self.tGraph[logHash] = [bundle.branch, bundle.trunk]
                    self.tData[logHash] = {'data_payload': bundle.data_payload,
                                                     'value_payload': bundle.outputTrxn.value}
                    self.tValues[logHash] = bundle.data_payload
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
    def check_value_tx(self,bundle):
        if bundle.inputTrxn.senderAddr in self.tLedger:
            # Check if sender has the crypto...
            if abs(bundle.inputTrxn.value) <= self.tLedger[bundle.inputTrxn.senderAddr]:
                res = True
        return res

    # Moves crypto from a sender to a receiver account
    def move_money(self,bundle):
        sendNode = None
        recNode = None

        for node in self.netNodes:
            if node.address == bundle.inputTrxn.senderAddr:
                sendNode = node

        for node in self.netNodes:
            if node.address == bundle.outputTrxn.recAddr:
                recNode = node

        self.tLedger[bundle.inputTrxn.senderAddr] += bundle.inputTrxn.value
        sendNode.bal += bundle.inputTrxn.value
        self.tLedger[bundle.outputTrxn.recAddr] += bundle.outputTrxn.value
        recNode.bal += bundle.outputTrxn.value