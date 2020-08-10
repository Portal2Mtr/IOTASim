

# published in https://medium.com/@stkubr/simple-directed-acyclic-graph-iota-like-implementation-in-python-8e07677c55b5

from tangle import Tangle
from sim_env_file import simEnv
import random
import logging
logger = logging.getLogger(__name__)


def configure_logging():
    root_logger = logging.getLogger()
    console = logging.StreamHandler()

    formatter = logging.Formatter(
        "[%(filename)s] %(asctime)s %(levelname)-8s %(message)s"
    )

    # add the formatter to the console handler, and the console handler to the root logger
    console.setFormatter(formatter)
    for hdlr in root_logger.handlers:
        root_logger.removeHandler(hdlr)
    root_logger.addHandler(console)

    # set logging level for root logger
    root_logger.setLevel("INFO")


if __name__ == "__main__":
    configure_logging()
    logger.info("Setting up environment...")
    # Initialize Objects for Simulation
    myTangle = Tangle()
    workEnv = simEnv(myTangle)
    networkNodes = []

    # Main tangle actors
    logger.info("Establishing main tangle actors...")
    charlesNode = workEnv.createNode(myTangle,"charles",initBal=50)
    satoshiNode = workEnv.createNode(myTangle,"satoshi",initBal=100)
    jagNode = workEnv.createNode(myTangle,"drjag",initBal=200)
    ericNode = workEnv.createNode(myTangle,"eric",initBal=25)
    emilyNode = workEnv.createNode(myTangle,"emily",initBal=500)

    # Build tangle

    # TODO: Create discrete-time script of adding to tangle (back-burner)
    numTrxns = 20
    logger.info("Building basic tangle with " + str(numTrxns) + " trxns...")
    for i in range(numTrxns):
        selectInt = random.randint(0, len(workEnv.simNodes) - 1)
        workEnv.addTrxn(myTangle, workEnv.simNodes[selectInt])
        workEnv.addTrxn(myTangle, charlesNode)

    #Print Ledger with Trxns
    logger.info("Tangle initialization done!")
    logger.info("Generating graph and GUI...")
    workEnv.genGraph()
    workEnv.mainloop()
    # workEnv.showTangleData()




