# Represents a simulation environment that simulates a tangle in IOTA.
# Simulation env assumes each IOTA node has the same view of the tangle.
# Also has several wrappers to simplify commands from main file

from tangle import Tangle
from block import Block
from iota_node import IOTANode
import networkx as NX
import matplotlib
import random

import networkx as nx
from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,StaticLayoutProvider,PanTool)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

class simEnv:

    def setupWindow(self,tangle,node):
        self.workingTangle = tangle

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

    def showTangleData(self):
        # Create graph with networkx, plot in matplotlib and put in tkinter window
        G = NX.DiGraph()

        trxns = self.workingTangle.tGraph
        # genList = []
        genPosX = 50
        genPos1 = 900
        genPos2 = 1100
        gotBranch = False
        tipCntr = 0
        # genPos = {'genesis_branch':[50,900],'genesis_trunk':[50,1100]}
        for key,values in trxns.items():
            if len(values) == 0:
                # Genesis block
                G.add_node(key,posX=genPosX,posY=genPos1 if not gotBranch else genPos2,nodeIdx='Genesis',hash="N/A")
                gotBranch = True
                # genList.append(key)
            else:
                # nongenesis block
                G.add_node(key,posX=0,posY=0,nodeIdx=tipCntr,hash=key)
                tipCntr += 1
                for entry in values:
                    G.add_edge(key,entry)

                xMax = 0
                for neighbor in G.neighbors(key):
                    workX = G.nodes[neighbor]['posX']
                    xMax = workX if workX > xMax else xMax

                xMax += 100
                nodeY = random.randint(700,1300)
                G.nodes[key]['posX'] = xMax
                G.nodes[key]['posY'] = nodeY

        genPos = {}
        genList = []
        for node in G.nodes:
            genList.append(node)
            genPos[node] = [G.nodes[node]['posX'], G.nodes[node]['posY']]


        # Setup renderer
        graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
        fixed_layout = genPos
        fixed_layout_provider = StaticLayoutProvider(graph_layout=fixed_layout)
        graph_renderer.layout_provider = fixed_layout_provider
        graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
        graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=1)

        # Show with Bokeh
        plot = Plot(plot_width=1000, plot_height=1000,
                    x_range=Range1d(0, 1000), y_range=Range1d(500, 2000))
        plot.title.text = "Graph Interaction Demonstration"
        node_hover_tool = HoverTool(tooltips=[("nodeIdx", "@nodeIdx"),("hash","@hash")])
        plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool(),PanTool())
        plot.renderers.append(graph_renderer)
        output_file("interactiveGUI.html")
        show(plot)


