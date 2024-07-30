
module test_tb;
    
    // Inputs
    reg clock1;
    reg clock2;
    reg rst;
    reg enable;
    reg next;
    reg [3:0] data_in;
    reg [3:0] decre_in;

    // Outputs
    wire [3:0] data_out;

    // Instantiate DUT (Design Under Test)
    test dut (
        .clock1(clock1),
        .clock2(clock2),
        .rst(rst),
        .enable(enable),
        .next(next),
        .data_in(data_in),
        .decre_in(decre_in),
        .data_out(data_out)
    );

    // Initial Block
    initial begin
    // VCD Dump commands
    $dumpfile("test_tb.vcd");  // Specify the name of the VCD file
    $dumpvars(0, test_tb);  // Dump variables from the testbench module
        clock1 = 0;
        clock2 = 0;
        enable = 0;
        next = 0;
        data_in = 0;
        decre_in = 0;
        rst = 1;
        #10 rst = 0;
        data_in = 10;
        decre_in = 12;
        #100;  // Simulation end time
        $finish;
    end
    // always block initialisation
    always #10 begin if ( data_in > 3) begin data_in = data_in + 1; end end
    always #10 begin if (decre_in > 0) begin decre_in = decre_in - 1; end end
    
    // Clock Generation
    always #(4.0) clock1 = ~clock1;
    always #(10.0) clock2 = ~clock2;


endmodule
