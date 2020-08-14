#!/usr/bin/env python

"""Python IOTA DAG Simulator

Simulates a simple Directed Acyclic Graph (DAG) based on IOTA using the same protocol specs. Has a simple tKinter GUI
and generates the DAG in matplotlib.

Started from simple iota tutorial and expanded upon with functions from official Python IOTA API client.
Published in https://medium.com/@stkubr/simple-directed-acyclic-graph-iota-like-implementation-in-python-8e07677c55b5

"""

from tangle import Tangle
from sim_env_file import simEnv
import random
import logging
logger = logging.getLogger(__name__)

__author__ = "Charles Rawlins"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Charles Rawlins"
__email__ = "crfmb@mst.edu"
__status__ = "Prototype"


def configure_logging():
    """Configures the logger for the entire project.

    Use logger.info() to log information.

    :return: None
    """
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
    # Configure logger for logging...
    configure_logging()
    logger.info("Setting up environment...")
    # Initialize Objects for Simulation
    myTangle = Tangle()
    workEnv = simEnv(myTangle)
    networkNodes = []

    # Generate simple main tangle actors
    logger.info("Establishing main tangle actors...")
    charlesNode = workEnv.createNode(myTangle,"charles",initBal=50)
    satoshiNode = workEnv.createNode(myTangle,"satoshi",initBal=100)
    jagNode = workEnv.createNode(myTangle,"drjag",initBal=200)
    ericNode = workEnv.createNode(myTangle,"eric",initBal=25)
    emilyNode = workEnv.createNode(myTangle,"emily",initBal=500)

    # Build tangle with empty trxns
    numTrxns = 5
    logger.info("Building basic tangle with " + str(numTrxns) + " trxns...")
    for i in range(numTrxns):
        logger.info("Generating {}/{}...".format(i+1,numTrxns))
        selectInt = random.randint(0, len(workEnv.simNodes) - 1)
        workEnv.addTrxn(myTangle, workEnv.simNodes[selectInt])

    #Print Ledger with Trxns
    logger.info("Tangle initialization done!")
    logger.info("Generating graph and GUI...")
    workEnv.genGraph()
    workEnv.mainloop()
