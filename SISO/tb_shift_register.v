module tb_shift_register;

reg clk;
reg reset;
reg load;
reg enable;
reg [7:0] data_in;
wire [7:0] shift_reg;
wire serial_out;
reg serial_in;

initial begin
    $from_myhdl(
        clk,
        reset,
        load,
        enable,
        data_in,
        serial_in
    );
    $to_myhdl(
        shift_reg,
        serial_out
    );
end

shift_register dut(
    clk,
    reset,
    load,
    enable,
    data_in,
    shift_reg,
    serial_out,
    serial_in
);

endmodule
