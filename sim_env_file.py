# Represents a simulation environment that simulates a tangle in IOTA.
# Simulation env assumes each IOTA node has the same view of the tangle.
# Also has several wrappers to simplify commands from main file
from bundle import Bundle
from iota_node import IOTANode
import networkx as NX
import matplotlib.pyplot as plt
from trxn import Trxn
import tkinter as tk
import random
global fig, ax
import copy
import logging
logger = logging.getLogger(__name__)

# Class used for simulation environment for Tangle and nodes generating 'simple' transactions.
class simEnv(tk.Tk):

    def __init__(self,tangle, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("500x200")
        self.label = tk.Label(text="DAG Simulation GUI")
        self.label.pack(padx=10, pady=10)
        self.addButton = tk.Button(text="Add Blank Meta Transaction",command=self.addTangleTrxn)
        self.addButton.pack()
        self.dispButton = tk.Button(text="Display Tangle",command=self.showTangleData)
        self.dispButton.pack()
        self.moveButton = tk.Button(text="Move Random Currency",command=self.moveCryptoExample)
        self.moveButton.pack()
        self.title("DAG Example GUI")
        self.simNodes = []
        self.workingTangle = tangle
        self.firstDraw = True

    # Wrapper for adding trxn to tangle
    def addTrxn(self,workTangle,workNode):
        tips = workTangle.find_tips()
        tipObjs = []
        for tip in tips:
            tipObjs.append(workTangle.bundleObjects.get(tip))

        genBundle = Bundle(tips,tipObjs, workNode) # Generate basic bundle
        metaTrxn = Trxn(genBundle)
        genBundle.addTrxn(metaTrxn) # Add non-value trxn
        workTangle.add_tx(genBundle) # Record bundle with transaction in tangle and do PoW

    # Wrapper for adding real-value transaction to tangle
    def addTrxnTransfer(self,workTangle,sendNode,recNode,transAmount=5):
        tips = workTangle.find_tips()
        tipObjs = []
        for tip in tips:
            tipObjs.append(workTangle.bundleObjects.get(tip))

        value_bundle = Bundle(workTangle.find_tips(),tipObjs, sendNode)
        # add value transition in Bundle
        value_bundle.add_value_tx(sendNode, recNode, transAmount)
        workTangle.add_tx(value_bundle)

    # Wrapper for creating node on tangle quickly
    def createNode(self,workTangle,name,initBal=50):
        workNode = IOTANode(name, initBal=initBal)
        workTangle.initLedger(workNode)
        self.simNodes.append(workNode)
        return workNode

    # Generate networkx graph from tangle data
    def genGraph(self):
        # Create graph with networkx, plot in matplotlib
        G = NX.DiGraph()
        trxns = self.workingTangle.tGraph
        self.oldTrxns = copy.deepcopy(trxns)
        genPosX = 50
        genPos1 = 900
        genPos2 = 1100
        gotBranch = False
        tipCntr = 0

        for key, values in trxns.items():
            if values[0] is None:
                # Genesis transaction
                G.add_node(key, posX=genPosX, posY=genPos1 if not gotBranch else genPos2, nodeIdx='Genesis', hash="N/A")
                gotBranch = True
                # genList.append(key)
            else:
                # nongenesis transaction
                G.add_node(key, posX=0, posY=0, nodeIdx=tipCntr, hash=key)
                tipCntr += 1
                for entry in values:
                    G.add_edge(key, entry)

                xMax = 0
                for neighbor in G.neighbors(key):
                    workX = G.nodes[neighbor]['posX']
                    xMax = workX if workX > xMax else xMax

                # Place new node randomly in front of transactions it is referencing
                xMax += 100
                nodeY = random.randint(700, 1300)
                G.nodes[key]['posX'] = xMax
                G.nodes[key]['posY'] = nodeY

        self.drawGraph = G
        self.oldCntr = tipCntr

    # Updates graph for plotting with new transactions
    def updateGraph(self):
        # Create graph with networkx, plot in matplotlib
        G = self.drawGraph
        oldTrxns = self.oldTrxns
        trxns = copy.deepcopy(self.workingTangle.tGraph)
        tempDict = {}
        for key, values in trxns.items():
            if key not in oldTrxns:
                tempDict[key] = values

        tipCntr = self.oldCntr
        for key, values in tempDict.items():
            # nongenesis blocks
            G.add_node(key, posX=0, posY=0, nodeIdx=tipCntr, hash=key)
            tipCntr += 1
            for entry in values:
                G.add_edge(key, entry)

            xMax = 0
            for neighbor in G.neighbors(key):
                workX = G.nodes[neighbor]['posX']
                xMax = workX if workX > xMax else xMax

            xMax += 100
            nodeY = random.randint(700, 1300)
            G.nodes[key]['posX'] = xMax
            G.nodes[key]['posY'] = nodeY

        self.drawGraph = G
        self.oldCntr = tipCntr
        self.oldTrxns = copy.deepcopy(trxns)

    # Shows the current networkx graph generated from tangle data
    def showTangleData(self):
        # Draw manually for live plotting
        if self.firstDraw:
            fig, ax = plt.subplots()
            ax.set_title("DAG View of Tansaction Tangle")
            self.ax = fig.add_subplot(1, 1, 1)
            self.firstDraw = False
        else:
            self.updateGraph()
            logger.info("Updated visual tangle!")
            fig, ax = plt.subplots()

        for node in self.drawGraph.nodes:
            ax.plot(self.drawGraph.nodes[node]['posX'],self.drawGraph.nodes[node]['posY'],
                            marker="o",color='b',zorder=1,markersize=10)

        for node in self.drawGraph.nodes:
            if "genesis" not in node:
                for tip in self.drawGraph.neighbors(node):
                    arrowWidth = 5
                    arrowX = self.drawGraph.nodes[tip]['posX'] - self.drawGraph.nodes[node]['posX']
                    arrowY = self.drawGraph.nodes[tip]['posY'] - self.drawGraph.nodes[node]['posY']
                    ax.arrow(self.drawGraph.nodes[node]['posX'],self.drawGraph.nodes[node]['posY'],
                                 arrowX,arrowY,head_width=arrowWidth,head_length=7,length_includes_head=True,fc="k",ec="k",zorder=2)

        for node in self.drawGraph.nodes:
            if "genesis" in node:
                textX = 25
                textY = 10
                ax.text(self.drawGraph.nodes[node]['posX'] - textX,self.drawGraph.nodes[node]['posY'] + textY,node)
            else:
                textX = 25
                textY = 10
                ax.text(self.drawGraph.nodes[node]['posX'] - textX, self.drawGraph.nodes[node]['posY'] + textY,
                            node[0:8])

                if node in self.workingTangle.tValues:
                    textX = 25
                    textY = -40
                    ax.text(self.drawGraph.nodes[node]['posX'] - textX, self.drawGraph.nodes[node]['posY'] + textY,
                            self.workingTangle.tValues[node],c='g')

        plt.draw()
        plt.axis("off")
        plt.show()


    # Adds transaction to Tangle from tkinter gui
    def addTangleTrxn(self):
        selectInt = random.randint(0, len(self.simNodes) - 1)
        self.addTrxn(self.workingTangle,self.simNodes[selectInt])
        logger.info("Added trxn from node " + self.simNodes[selectInt].name + "!")


    # Moves crypto between two random nodes with tkinter gui
    def moveCryptoExample(self):
        fromInt = random.randint(0, len(self.simNodes) - 1)
        toInt = random.randint(0, len(self.simNodes) - 1)
        while toInt == fromInt:
            toInt = random.randint(0, len(self.simNodes) - 1)

        logger.info("Moving crypto from " + self.simNodes[fromInt].name + " to " + self.simNodes[toInt].name + "...")
        self.addTrxnTransfer(self.workingTangle, self.simNodes[fromInt], self.simNodes[toInt])
        logger.info("Moved " + str(5) + " crypto from " + self.simNodes[fromInt].name + " to " + self.simNodes[toInt].name + "!")



