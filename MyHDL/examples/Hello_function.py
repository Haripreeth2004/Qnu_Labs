from myhdl import block,delay,instance,always,now
@block
def Hello(clk, to="World!"):

    @always(clk.posedge)
    def say_hello():
        print("%s Hello %s" % (now(), to))

    return say_hello