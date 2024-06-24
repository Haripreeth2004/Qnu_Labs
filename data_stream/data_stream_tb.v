`timescale 1ns/1ps

module testbench;

reg clk;
reg rst;
wire data_out;

// Instantiate the data_stream module
data_stream uut (
    .clk(clk),
    .rst(rst),
    .data_out(data_out)
);

// Clock generation
initial begin
    clk = 0;
    forever #5 clk = ~clk; // 100MHz clock
end

// Test sequence
initial begin
    // Open VCD file for dumping
    $dumpfile("data_stream.vcd");
    $dumpvars(0, testbench);

    // Initialize
    rst = 1;
    #10;

    // Release reset
    rst = 0;

    // Run simulation for 200ns
    #200;

    // End simulation
    $finish;
end

endmodule
