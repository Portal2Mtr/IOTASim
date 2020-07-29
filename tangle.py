import random
from block import Block
# Manages the tangle in its entirety, several tangle Nodes and many blocks.
class Tangle:
    def __init__(self):
        # Two tips to start TODO: one is realistic?
        self.tGraph = {'genesis_branch': [],
                'genesis_trunk': []
                }

        # No data to start
        self.tData = {}

        # Five nodes for example TODO: make IOTA nodes
        self.tLedger = {}
        self.netNodes = []

    def initLedger(self,node):
        self.tLedger[node.name] = node.bal
        self.netNodes.append(node)

    def add_tx(self,block: Block):
        if block.branch in self.tGraph and block.trunk in self.tGraph:
            if block.value_tx:
                if self.check_value_tx(block.value_tx):
                    self.move_money(block.value_tx['senderID'],
                               block.value_tx['receiverID'],
                               block.value_tx['amount'])
                    self.tGraph[block.get_hash()] = [block.branch, block.trunk]
                    self.tData[block.get_hash()] = {'data_payload': block.data_payload,
                                                     'value_payload': block.value_tx}
            else:
                self.tGraph[block.get_hash()] = [block.branch, block.trunk]
                self.tData[block.get_hash()] = block.data_payload

    # Get tips from tangle randomly (normally MCMC in old IOTA, modified URTS in new IOTA)
    def find_tips(self):
        # TODO: Implement URTS
        return tuple(random.sample(set(self.tGraph.keys()), 2))

    def check_value_tx(self,value_tx):
        if value_tx['sender'] in self.tLedger:
            if value_tx['amount'] <= self.tLedger[value_tx['sender']]:
                # if signature is valid too
                res = True
        return res

    def move_money(self,sender, receiver, amount):
        self.tLedger[sender.name] -= amount
        sender.bal -= amount
        if receiver.name in self.tLedger:
            self.tLedger[receiver.name] += amount
            receiver.bal += amount
        else:
            self.tLedger[receiver.name] = amount
            receiver.bal += amount