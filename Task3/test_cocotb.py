import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.clock import Clock

import random

@cocotb.test()
async def test_piso(dut):
    clock = Clock(dut.clk, 10, units="ns")  # Create a 10ns period clock on port clk
    cocotb.start_soon(clock.start(start_high=False))
    
    # Reset the DUT
    dut.parallel_in.value = 0
    dut.enable.value = 0
    dut.load.value = 0
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    await Timer(100, units="ns")
    dut.reset.value = 0

    # Determine the width of the parallel_in signal
    signal_width = len(dut.parallel_in)
    cocotb.log.info(f"Detected parallel_in width: {signal_width} bits")
    # Adjust the delay based on the signal width
    load_delay = (signal_width * 10) - 10

    # Helper function to load and shift parallel data
    async def load_and_shift(parallel_value):
        dut.enable.value = 1
        dut.load.value = 1
        dut.parallel_in.value = parallel_value
        #cocotb.log.info(f"Before rising edge: parallel_in={int(dut.parallel_in.value)}, enable={int(dut.enable.value)}, load={int(dut.load.value)}, reset={int(dut.reset.value)}, shift_reg={int(dut.shift_reg.value)}")
        await RisingEdge(dut.clk)
        await Timer(10, units="ns")
        dut.load.value = 0
        assert dut.shift_reg.value == parallel_value, f"Shift reg value mismatch after loading {parallel_value}: {int(dut.shift_reg.value)}"
        assert dut.load.value == 1,f"Load value is not high"
        assert dut.enable ==1,f"Enable value is not high"
        cocotb.log.info(f"After load deassert: parallel_in={int(dut.parallel_in.value)}, enable={int(dut.enable.value)}, load={int(dut.load.value)}, reset={int(dut.reset.value)}, shift_reg={int(dut.shift_reg.value)}")
        await RisingEdge(dut.clk)
        #cocotb.log.info(f"After second rising edge: parallel_in={int(dut.parallel_in.value)}, enable={int(dut.enable.value)}, load={int(dut.load.value)}, reset={int(dut.reset.value)}, shift_reg={int(dut.shift_reg.value)}")
        #await Timer(70,units="ns")  
        await Timer(load_delay,units="ns")
        dut.enable.value = 0
        await Timer(20, units="ns")

    # List to store shift_reg values
    shift_reg_values = []

    # Function to capture shift_reg value on every rising edge of the clock
    async def capture_shift_reg():
        while True:
            await RisingEdge(dut.clk)
            shift_reg_values.append(int(dut.shift_reg.value))
            cocotb.log.info(f"Time: {cocotb.utils.get_sim_time(units='ns')}, Shift reg value: {int(dut.shift_reg.value)}")

    # Start capturing shift_reg values
    cocotb.start_soon(capture_shift_reg())

    # Load and shift first value
    await load_and_shift(150)
    await load_and_shift(98)
    await load_and_shift(221)

    # Randomized Testing
    max_value = (1 << signal_width) - 1
    for _ in range(10):
        random_value = random.randint(0, max_value)
        #await load_and_shift(random_value)

    # Print all captured shift_reg values
    print("Captured shift_reg values:", shift_reg_values)

    
