# Represents a simulation environment that simulates a tangle in IOTA.
# Simulation env assumes each IOTA node has the same view of the tangle.
# Also has several wrappers to simplify commands from main file

from tangle import Tangle
from block import Block
from iota_node import IOTANode
class simEnv:
    def __init__(self):
        self.myvar = 0

    # Wrapper for adding trxn to tangle
    def addTrxn(self,workTangle,workNode):
        workTangle.add_tx(Block(workTangle.find_tips(), workNode))

    #Wrapper for adding real-value transaction to tangle
    def addTrxnTransfer(self,workTangle,sendNode,recNode,transAmount=5):
        value_block = Block(workTangle.find_tips(), sendNode)
        # add value transition in block
        value_block.add_value_tx(sendNode, recNode, transAmount)
        workTangle.add_tx(value_block)

    # Wrapper for creating node on tangle quickly
    def createNode(self,workTangle,name,initBal=50):
        workNode = IOTANode(name,name+"sig", initBal=initBal)
        workTangle.initLedger(workNode)
        return workNode