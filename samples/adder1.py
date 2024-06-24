from myhdl import block, always_comb, Signal, intbv, delay, instance, Simulation, toVHDL, ResetSignal,toVerilog

@block
def adder(a, b, c):
    @always_comb
    def logic():
        c.next = a + b
    return logic

@block
def testbench():
    a = Signal(intbv(0)[4:])
    b = Signal(intbv(0)[4:])
    c = Signal(intbv(0)[5:])  # Extra bit for overflow

    adder_inst = adder(a, b, c)

    @instance
    def stimulus():
        for i in range(4):
            for j in range(4):
                a.next = i
                b.next = j
                yield delay(1000)
                print(f"a = {a}, b = {b}, c = {c}")

    return adder_inst, stimulus

# Run the simulation
tb = testbench()
sim = Simulation(tb)
sim.run()

# Convert the adder to VHDL
a = Signal(intbv(0)[4:])
b = Signal(intbv(0)[4:])
c = Signal(intbv(0)[5:])
adder_inst = adder(a, b, c)
toVerilog(adder_inst, a, b, c)

# Convert the testbench to VHDL
tb = testbench()
tb.convert(hdl='Verilog')