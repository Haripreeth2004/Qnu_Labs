
module piso_shift_register_tb;

    // Inputs
    reg clk;
    reg enable;
    reg reset;
    reg load;
    reg [7:0] parallel_in;

    // Outputs
    wire [7:0] shift_reg;
    wire serial_out;

    // Instantiate DUT (Design Under Test)
    piso_shift_register dut (
        .clk(clk),
        .enable(enable),
        .reset(reset),
        .load(load),
        .parallel_in(parallel_in),
        .shift_reg(shift_reg),
        .serial_out(serial_out)
    );

    // Initial Block
    initial begin
        clk = 0;
        reset = 1;
        parallel_in = 0;
        load = 0;
        #100;
        reset = 0;

        
        // Automated test vectors
        #10 enable = 1;
        #10 reset = 0;
        #10 load = 1;
        parallel_in = 150;
        #80
        enable = 0;
        #20;


        #10 enable = 1;
        #10 reset = 0;
        #10 load = 1;
        parallel_in = 98;
        #80;
        enable = 0;
        #20;

        #10 enable = 1;
        #10 reset = 0;
        #10 load = 1;
        parallel_in = 0;
        #80;
        enable = 0;
        #20;

        #100;  // Simulation end time
        $finish;
    end

    // Clock Generation
    always #5 clk = ~clk;

endmodule
