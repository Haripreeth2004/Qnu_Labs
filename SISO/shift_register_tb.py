from myhdl import *
ACTIVE, INACTIVE = bool(0), bool(1)
from shift_register_design import shift_register

@block
def test_sftreg():
    clk,load,enable,serial_out,serial_in = [Signal(INACTIVE) for i in range (5)]
    data_in = Signal(intbv(0)[8:])
    reset = ResetSignal(val=1, active=0, isasync=True)
    shift_reg = Signal(intbv(0)[8:])
    """ Clock generator """
    @always(delay(10))
    def clkgen():
        clk.next = not clk
    # Instantiate the shift register
    shift_reg_inst = shift_register(clk, reset, load, enable, data_in, shift_reg,serial_out,serial_in)

    @instance
    def stimulus():
        """ Testbench stimulus """
        clk.next = 0
        reset.next = 1
        load.next = 0
        enable.next = 0
        data_in.next = 0

        # Wait for initial conditions
        yield delay(10)

        # Release reset
        reset.next = 0
        yield delay(80)

        # Load data into shift register
        load.next = 1
        data_in.next = 0xAA  # Example data
        yield delay(10)
        load.next = 0
        yield delay(80)

        enable.next = 1
        for bit in bin(data_in, 8):
            serial_in.next = int(bit)
            yield clk.negedge
        enable.next = 0

        
        # End simulation
        raise StopSimulation

    # Monitor process
    @always(clk.posedge)
    def monitor():
        print(f"[{now():>6}] clk={int(clk)}, reset={int(reset)}, load={int(load)}, enable={int(enable)}, data_in={hex(int(data_in))}, shift_reg={hex(int(shift_reg))}, serial_out={int(serial_out)}")

   

        raise StopSimulation
    return clkgen,stimulus,shift_reg_inst,monitor
    
    # Run the simulation
simInst = test_sftreg()
simInst.config_sim(trace=True, tracebackup=False)
simInst.run_sim()


def convert():
    # Signal declarations
    clk = Signal(bool(0))
    reset = ResetSignal(0, active=1, isasync=True)
    load = Signal(bool(0))
    enable = Signal(bool(0))
    data_in = Signal(intbv(0)[8:])
    serial_out = Signal(bool(0))
    shift_reg = Signal(intbv(0)[8:])
    serial_in = Signal(bool(0))  
     # Instantiate the shift register
    conshift_reg_inst = shift_register(clk, reset, load, enable, data_in,shift_reg,serial_out,serial_in)

    # Convert to Verilog
    conshift_reg_inst.convert(hdl='Verilog')

    # Convert to VHDL (if needed)
    # shift_reg_inst.convert(hdl='VHDL')

# Uncomment the following line to convert the design when this script is run
convert()