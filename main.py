# published in https://medium.com/@stkubr/simple-directed-acyclic-graph-iota-like-implementation-in-python-8e07677c55b5

from tangle import Tangle
from iota_node import IOTANode
from block import Block
from sim_env_file import simEnv

if __name__ == "__main__":

    # Initialize Objects for Simulation
    myTangle = Tangle()
    workEnv = simEnv(myTangle)
    networkNodes = []

    # Main tangle actors
    charlesNode = workEnv.createNode(myTangle,"charles",initBal=50)
    satoshiNode = workEnv.createNode(myTangle,"satoshi",initBal=100)
    jagNode = workEnv.createNode(myTangle,"drjag",initBal=200)
    ericNode = workEnv.createNode(myTangle,"eric",initBal=25)
    emilyNode = workEnv.createNode(myTangle,"emily",initBal=500)

    # Build tangle
    # TODO: Create discrete-time script of adding to tangle
    workEnv.addTrxn(myTangle,charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    workEnv.addTrxn(myTangle, charlesNode)
    # Create value transaction

    #Print Ledger with Trxns
    workEnv.genGraph()
    # workEnv.showTangleData()
    workEnv.mainloop()
    # workEnv.addTrxn(myTangle, charlesNode)
    # workEnv.addTrxn(myTangle, charlesNode)
    # workEnv.addTrxn(myTangle, charlesNode)
    # workEnv.addTrxn(myTangle, charlesNode)
    # workEnv.addTrxn(myTangle, charlesNode)
    # workEnv.showTangleData()



