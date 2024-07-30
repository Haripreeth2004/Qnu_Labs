//`timescale 1us/1ns
module piso_shift_register (
    input clk,
    input enable,
    input reset,
    output reg [7:0] shift_reg,
    input load, // Control signal to load parallel data
    input [7:0] parallel_in, // 8-bit parallel input
    output reg serial_out // Serial output
);
    always @(posedge clk) begin
        if (reset || !enable) begin
            shift_reg <= 8'b0;
            serial_out <= 1'b0;
        end else if (enable) begin
            if (load) begin
                shift_reg <= parallel_in;
            end else begin
                //{shift_reg, serial_out} <= {shift_reg[6:0],1'b0,shift_reg[6]}; Concurrent statement use this instead using procedural block
                shift_reg <= {shift_reg[6:0], 1'b0}; // Shift left and insert a 0 at LSB
                serial_out <= shift_reg[7]; // MSB is the serial output
            end
        end
    end
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(1, piso_shift_register);
    end
endmodule
