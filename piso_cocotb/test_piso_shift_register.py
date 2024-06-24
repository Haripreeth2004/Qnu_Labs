import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, ReadOnly, Timer
import random

# # @cocotb.coroutine
# # def reset_dut(dut):
# #     dut.reset.value = 1
# #     yield ClockCycles(dut.clk, 10)
# #     dut.reset.value = 0
# #     yield ClockCycles(dut.clk.value, 10)

# # @cocotb.coroutine
# # def clock_generator(dut):
# #     while True:
# #         dut.clk.value <= 0
# #         yield ClockCycles(dut.clk, 5)
# #         dut.clk.value <= 1
# #         yield ClockCycles(dut.clk, 5)

# # @cocotb.coroutine
# # def stimulus(dut):
# #     # Initialize signals
# #     dut.enable.value = 0
# #     dut.load.value = 0
# #     dut.parallel_in.value = 0

# #     # Start clock
# #     cocotb.start_soon(clock_generator(dut.clk))

# #     # Apply reset
# #     yield reset_dut(dut)

# #     # Test sequences
# #     for i in range(3):
# #         # Enable shift register operation
# #         dut.enable.value = 1

# #         # Load parallel data
# #         dut.parallel_in.value = random.randint(0, 255)
# #         dut.load.value = 1
# #         yield RisingEdge(dut.clk)
# #         dut.load.value = 0

# #         # Wait for shifting
# #         yield ClockCycles(dut.clk, 8)  # Wait for 8 clock cycles

# #         # Observe serial output
# #         serial_out = dut.serial_out.value.integer
# #         shift_reg = dut.shift_reg.value.integer
# #         print(f"Iteration {i+1}: Serial Out = {serial_out}, Shift Reg = {shift_reg}")

# #         # Disable shift register operation
# #         dut.enable.value = 0

# #         yield ClockCycles(dut.clk, 10)

# #     # Finish simulation
# #     yield ClockCycles(dut.clk, 10)
# #     raise cocotb.result.TestSuccess("Simulation complete")

# @cocotb.test()
# def test_piso_shift_register(dut):
#     """Testbench main function."""
#     yield stimulus(dut)

@cocotb.test()
async def test_piso_shift_register(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.fork(clock.start())
    
    dut.parallel_in.value = 0
    dut.load.value= 0
    dut.reset.value =1
    await RisingEdge(dut.clk)
    await cocotb.triggers.Timer(100, units="ns")
    dut.reset.value =0
    # 1st iteration
    dut.enable.value = 1
    dut.parallel_in.value = 126
    dut.load.value= 1
    await RisingEdge(dut.clk)
    dut.load.value= 0
    await RisingEdge(dut.clk)
    await Timer(80,units="ns")
    dut.enable.value = 0
    await Timer(20,units="ns")
    
    #2nd iteration
    dut.enable.value = 1
    dut.parallel_in.value = 98
    dut.load.value= 1
    await RisingEdge(dut.clk)
    dut.load.value= 0
    await RisingEdge(dut.clk)
    await Timer(80,units="ns")
    dut.enable.value = 0
    await Timer(20,units="ns")
    
    #3nd iteration
    dut.enable.value = 1
    dut.parallel_in.value = 221
    dut.load.value= 1
    await RisingEdge(dut.clk)
    dut.load.value= 0
    await RisingEdge(dut.clk)
    await Timer(80,units="ns")
    dut.enable.value = 0
    await Timer(20,units="ns")
    
    # Observe serial output
    serial_out = dut.serial_out.value
    shift_reg = dut.shift_reg.value
    # print(f" Serial Out: {serial_out}, Shift Reg: {shift_reg}")

    for t in range(20):
                
                dut.clk.value<=1
                await Timer(5,units="ns")
                dut.clk.value<=0
                await Timer(5,units="ns")