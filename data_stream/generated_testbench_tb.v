
module data_stream_tb;

    // Inputs
    reg clk;
    reg rst;

    // Outputs
    wire data_out;

    // Instantiate DUT (Design Under Test)
    data_stream dut (
        .clk(clk),
        .rst(rst),
        .data_out(data_out)
    );

    // Initial Block
    initial begin
        clk = 0;
        #10 rst = ~rst;


        #10 rst = ~rst;


        #10 rst = ~rst;



        #100;  // Simulation end time
        $finish;
    end

    // Clock Generation
    always #5 clk = ~clk;

endmodule
