
module piso_shift_register_tb;
    
    // Inputs
    reg clock;
    reg clk1;
    reg clk2;
    reg enable;
    reg reset;
    reg rstn;
    reg load;
    reg [7:0] parallel_in;
    reg [3:0] serial_in;
    reg [3:0] decre_in;
    reg [7:0] data1;
    reg [15:0] High_data;
    reg data2;
    reg reset1;

    // Outputs
    wire [7:0] shift_reg;
    wire serial_out;

    // Instantiate DUT (Design Under Test)
    piso_shift_register dut (
        .clock(clock),
        .clk1(clk1),
        .clk2(clk2),
        .enable(enable),
        .reset(reset),
        .rstn(rstn),
        .load(load),
        .parallel_in(parallel_in),
        .serial_in(serial_in),
        .decre_in(decre_in),
        .data1(data1),
        .High_data(High_data),
        .data2(data2),
        .reset1(reset1),
        .shift_reg(shift_reg),
        .serial_out(serial_out)
    );

    // Initial Block
    initial begin
    // VCD Dump commands
    $dumpfile("piso_shift_register_tb.vcd");  // Specify the name of the VCD file
    $dumpvars(0, piso_shift_register_tb );  // Dump variables from the testbench module
        clock = 0;
        clk1 = 0;
        clk2 = 0;
        enable = 0;
        load = 0;
        parallel_in = 0;
        serial_in = 0;
        decre_in = 0;
        data1 = 0;
        High_data = 0;
        reset = 0;
        #10 reset = 1;
        rstn = 1;
        #10 rstn = 0;
        reset1 = 1;
        #10 reset1 = 0;
        parallel_in = 184;
        serial_in = 11;
        decre_in = 0;
        data1 = 125;
        #10 data1 = 96;
        #10 data1 = 216;
        #10 data1 = 221;
        High_data = 13170;
        #10 High_data = 64632;
        #10 High_data = 27579;
        #10 High_data = 43055;
        data2 = 1;
        #10 data2 = 1;
        #10 data2 = 1;
        #10 data2 = 0;
        #100;  // Simulation end time
        $finish;
    end
    // always block initialisation
    always #10 begin if ( parallel_in > 3) begin parallel_in = parallel_in + 1; end end
    always #10 begin if ( serial_in > 3) begin serial_in = serial_in + 1; end end
    always #10 begin if (decre_in > 0) begin decre_in = decre_in - 1; end end
    
    // Clock Generation
    always #(200.0) clock = ~clock;
    always #(50.0) clk1 = ~clk1;
    always #(100.0) clk2 = ~clk2;


endmodule
