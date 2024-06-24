from myhdl import block, always, instance, delay, StopSimulation, Signal, intbv, Cosimulation

# Define Verilog module code
verilog_code = """
module piso_shift_register(
    input wire clk,
    input wire enable,
    input wire reset,
    output reg [7:0] shift_reg,
    input wire load,
    input wire [7:0] parallel_in,
    output wire serial_out
);
    always @(posedge clk) begin
        if (reset) begin
            shift_reg <= 8'b0;
        end 
        else if (enable) begin
            if (load) begin
                shift_reg <= parallel_in;
            end else begin
                shift_reg <= {shift_reg[6:0], 1'b0};
            end
        end
    end

    assign serial_out = shift_reg[7];
endmodule
"""

# Save Verilog code to a file
verilog_file = "Piso_sample.v"
with open(verilog_file, "w") as f:
    f.write(verilog_code)

# Define MyHDL testbench
@block
def tb_piso_shift_register():
    clk = Signal(bool(0))
    enable = Signal(bool(0))
    reset = Signal(bool(0))
    load = Signal(bool(0))
    parallel_in = Signal(intbv(0)[8:])
    serial_out = Signal(bool(0))
    shift_reg = Signal(intbv(0)[8:])

    # Verilog compilation and simulation command
    verilog_cmd = f"iverilog -o piso_shift_register.o {verilog_file}"
    simulation_cmd = "vvp piso_shift_register.o"
    dut = Cosimulation(verilog_cmd,
                       clk=clk,
                       enable=enable,
                       reset=reset,
                       load=load,
                       parallel_in=parallel_in,
                       serial_out=serial_out,
                       shift_reg=shift_reg,
                       simulation_cmd=simulation_cmd)

    # Clock generation
    @always(delay(5))
    def clkgen():
        clk.next = not clk

    # Stimulus generation
    @instance
    def stimulus():
        print("enable reset load clk shift_reg serial_out")
        print("------------------------------------------")

        # Apply reset
        reset.next = 1
        yield delay(10)
        reset.next = 0
        yield delay(10)

        # Apply enable
        enable.next = 1
        yield delay(10)

        # Load parallel data
        parallel_in.next = intbv(0b10101010)[8:]
        load.next = 1
        yield delay(10)
        load.next = 0

        # Monitor signals
        yield delay(60)
        yield monitor()

        # Load new parallel data
        parallel_in.next = intbv(0b11110000)[8:]
        load.next = 1
        yield delay(10)
        load.next = 0

        # Monitor signals
        yield delay(40)
        yield monitor()

        # Load new parallel data
        parallel_in.next = intbv(0b11001011)[8:]
        load.next = 1
        yield delay(10)
        load.next = 0

        # Monitor signals
        yield delay(80)

        # Finish simulation
        raise StopSimulation

    # Monitor process
    @instance
    def monitor():
        while True:
            yield clk.negedge
            yield delay(1)
            print(f"{int(enable)} {int(reset)} {int(load)} {int(clk)} {bin(shift_reg, 8)} {int(serial_out)}")

    return dut, clkgen, stimulus, monitor

# Main function to run simulation
def simulate():
    tb = tb_piso_shift_register()
    tb.config_sim(trace=True)
    tb.run_sim()

if __name__ == "__main__":
    simulate()
