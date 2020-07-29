# Represents a simulation environment that simulates a tangle in IOTA.
# Simulation env assumes each IOTA node has the same view of the tangle.
# Also has several wrappers to simplify commands from main file

from tangle import Tangle
from block import Block
from iota_node import IOTANode
from tkinter import *
import networkx as NX
import matplotlib
import random
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpld3



class simEnv:

    def setupWindow(self,tangle,node):
        mainWindow = Tk()
        mainWindow.title("IOTA Simulation")
        globalX = 2000
        globalY = 1000
        mainWindow.geometry([str(globalX) + "x" + str(globalY)])

        # Setup Basic Frames
        inputX = 200
        graphX = globalX - inputX - inputX / 2
        inputY = globalY
        # inputFrame = Frame(mainWindow, width=inputX, height=inputY, background="#828282")
        # graphFrame = Frame(mainWindow, width=graphX, height=inputY, background="#4287f5")
        # graphFrame.place(x=0, y=0)
        # inputFrame.place(x=graphX, y=0)
        #
        # # Setup Widgets
        # widgetWidth = 50
        # selectLabel = Label(inputFrame, text="User Options:")
        # selectLabel.pack()
        # # TODO: add drawing functionality to adding trxn
        # trxnButton = Button(inputFrame, text="Add trxn", command=lambda: self.addTrxn(tangle,node))
        # trxnButton.pack()

        # tempLabel = Label(graphFrame,text="MEMES")
        # tempLabel.place(x=50,y=500)

        self.workingWindow = mainWindow
        self.workingTangle = tangle
        return mainWindow

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
                G.add_node(key,posX=genPosX,posY=genPos1 if not gotBranch else genPos2)
                gotBranch = True
                # genList.append(key)
            else:
                # nongenesis block
                G.add_node(key,posX=0,posY=0)
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


        # Relabel hash nodes for easier viewing

        f = plt.Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        pos = NX.spring_layout(G,fixed=genList,pos=genPos)

        NX.draw(G, pos, ax=a)
        NX.draw_networkx_labels(G,pos,ax=a)
        ######################

        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=self.workingWindow)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


        # button = Tk.Button(master=root, text='Quit', command=sys.exit)
        # button.pack(side=Tk.BOTTOM)


