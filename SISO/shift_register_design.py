from myhdl import *
ACTIVE, INACTIVE = bool(0), bool(1)

@block
def shift_register(clk, reset, load, enable, data_in,shift_reg,serial_out,serial_in):
    """
    8-bit shift register with load and enable functionality.
    
    Parameters:
    clk -- Clock signal
    reset -- Active high reset signal
    load -- Load signal to load data into shift register
    enable -- Enable signal to shift data
    data_in -- 8-bit parallel data input
    serial_out -- Serial data output
    """
    #run = Signal(bool(0))
    @always_seq(clk.posedge, reset=reset)
    def seq_logic():
            if (clk):
                    if reset:
                        shift_reg.next = intbv(0)[8:]
                    else:
                        if (load):
                            shift_reg.next = data_in
                        if (enable):
                            shift_reg.next = (shift_reg[7:1] << 1) | serial_in
                        else:
                            shift_reg.next = shift_reg
    @always_comb
    def output_logic():
        serial_out.next = shift_reg[0]

    return seq_logic, output_logic


