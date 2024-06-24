from myhdl import block, Signal

from parameter_ports import ClockDriver
from Hello_function import Hello


@block
def Greetings():

    clk1 = Signal(0)
    clk2 = Signal(0)

    clkdriver_1 = ClockDriver(clk1)  # positional and default association
    clkdriver_2 = ClockDriver(clk=clk2, period=10)  # named association
    hello_1 = Hello(clk=clk1)  # named and default association
    hello_2 = Hello(to="MyHDL", clk=clk2)  # named association

    return clkdriver_1, clkdriver_2, hello_1, hello_2


inst = Greetings()
inst.run_sim(50)