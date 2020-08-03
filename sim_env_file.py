# Represents a simulation environment that simulates a tangle in IOTA.
# Simulation env assumes each IOTA node has the same view of the tangle.
# Also has several wrappers to simplify commands from main file

from tangle import Tangle
from block import Block
from iota_node import IOTANode
import networkx as NX
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
import tkinter as tk
import random
import networkx as nx
from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,StaticLayoutProvider,PanTool,Button, CustomJS, ColumnDataSource)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx
from bokeh.layouts import *
import time
global fig, ax

class simEnv(tk.Tk):

    def __init__(self,tangle, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("500x500")
        self.label = tk.Label(text="DAG Simulation GUI")
        self.label.pack(padx=10, pady=10)
        self.addButton = tk.Button(text="Add trxn",command=self.GUIButtonFunc)
        self.addButton.pack()
        self.dispButton = tk.Button(text="Display Tangle",command=self.showTangleData)
        self.dispButton.pack()
        self.moveButton = tk.Button(text="Move Currency",command=self.moveMoneyExample)
        self.moveButton.pack()
        self.title("DAG Example GUI")
        self.simNodes = []
        self.workingTangle = tangle
        self.firstDraw = True


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
        self.simNodes.append(workNode)
        return workNode

    def genGraph(self):
        # Create graph with networkx, plot in matplotlib
        G = NX.DiGraph()

        trxns = self.workingTangle.tGraph
        # genList = []
        genPosX = 50
        genPos1 = 900
        genPos2 = 1100
        gotBranch = False
        tipCntr = 0
        # genPos = {'genesis_branch':[50,900],'genesis_trunk':[50,1100]}
        for key, values in trxns.items():
            if len(values) == 0:
                # Genesis block
                G.add_node(key, posX=genPosX, posY=genPos1 if not gotBranch else genPos2, nodeIdx='Genesis', hash="N/A")
                gotBranch = True
                # genList.append(key)
            else:
                # nongenesis block
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


    def showTangleData(self):
        # Draw manually for live plotting
        if self.firstDraw:
            fig, ax = plt.subplots()
            ax.set_title("DAG View of Tansaction Tangle")
            self.ax = fig.add_subplot(1, 1, 1)

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
                    textX = 15
                    textY = 10
                    ax.text(self.drawGraph.nodes[node]['posX'] - textX, self.drawGraph.nodes[node]['posY'] + textY,
                            node[0:8])

            self.firstDraw = False

        else:

            self.genGraph()
            fig, ax = plt.subplots()

            for node in self.drawGraph.nodes:
                ax.plot(self.drawGraph.nodes[node]['posX'], self.drawGraph.nodes[node]['posY'], marker="o",
                             color='b', zorder=1, markersize=10)

            for node in self.drawGraph.nodes:
                if "genesis" not in node:
                    for tip in self.drawGraph.neighbors(node):
                        arrowWidth = 5
                        arrowX = self.drawGraph.nodes[tip]['posX'] - self.drawGraph.nodes[node]['posX']
                        arrowY = self.drawGraph.nodes[tip]['posY'] - self.drawGraph.nodes[node]['posY']
                        ax.arrow(self.drawGraph.nodes[node]['posX'], self.drawGraph.nodes[node]['posY'],
                                      arrowX, arrowY, head_width=arrowWidth, head_length=7, length_includes_head=True,
                                      fc="k", ec="k", zorder=2)

            for node in self.drawGraph.nodes:
                if "genesis" in node:
                    textX = 25
                    textY = 10
                    ax.text(self.drawGraph.nodes[node]['posX'] - textX, self.drawGraph.nodes[node]['posY'] + textY,
                                 node)
                else:
                    textX = 15
                    textY = 10
                    ax.text(self.drawGraph.nodes[node]['posX'] - textX, self.drawGraph.nodes[node]['posY'] + textY,
                                 node[0:8])

        plt.draw()
        plt.axis("off")
        plt.show()


    def GUIButtonFunc(self):
        selectInt = random.randint(0, len(self.simNodes) - 1)
        self.addTrxn(self.workingTangle,self.simNodes[selectInt])
        print("Added trxn from node " + self.simNodes[selectInt].name + "!")

    def moveMoneyExample(self):

        fromInt = random.randint(0, len(self.simNodes) - 1)
        toInt = random.randint(0, len(self.simNodes) - 1)
        self.addTrxnTransfer(self.workingTangle, self.simNodes[fromInt], self.simNodes[toInt], 25)
        print("Moved " + str(25) + " crypto from " + self.simNodes[fromInt].name + " to " + self.simNodes[toInt].name + "!")



