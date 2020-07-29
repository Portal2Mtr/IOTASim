# published in https://medium.com/@stkubr/simple-directed-acyclic-graph-iota-like-implementation-in-python-8e07677c55b5

from tangle import Tangle
from iota_node import IOTANode
from block import Block
from sim_env_file import simEnv

if __name__ == "__main__":
    # Initialize Objects for Simulation
    workEnv = simEnv()
    myTangle = Tangle()
    networkNodes = []
    charlesNode = workEnv.createNode(myTangle,"charles",initBal=50)
    satoshiNode = workEnv.createNode(myTangle,"satoshi",initBal=100)

    # Build tangle
    # TODO: Create discrete-time script of adding to tangle
    workEnv.addTrxn(myTangle,charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)

    # Create value transaction
    workEnv.addTrxnTransfer(myTangle,charlesNode,satoshiNode,25)

    # TODO: Create visual graph of transactions
    #Print Ledger with Trxns
    print(myTangle.tData)

