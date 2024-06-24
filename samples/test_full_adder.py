# test_full_adder.py
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.result import TestFailure

@cocotb.test()
async def test_full_adder(dut):
    dut.A <= 0
    dut.B <= 0
    dut.Cin <= 0
    await FallingEdge(dut.clk)
    assert dut.Sum == 0 and dut.Cout == 0

    dut.A <= 1
    dut.B <= 1
    dut.Cin <= 0
    await FallingEdge(dut.clk)
    assert dut.Sum == 0 and dut.Cout == 1

    # Add more test cases as needed
