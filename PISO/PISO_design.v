
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
