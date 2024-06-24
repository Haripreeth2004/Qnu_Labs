import os

from myhdl import Cosimulation

cmd = "iverilog -o Cosimulation.o" + \
      "/workspaces/Qnu_Labs/JC2/johnCnt.v " + \
      "/workspaces/Qnu_Labs/JC2/johnCnt.tb.v "

def Simulation():
    return Cosimulation("vvp -m ../myhdl.vpi Cosimulation.o")