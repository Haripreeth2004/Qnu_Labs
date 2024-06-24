module data_stream(
    input wire clk,
    input wire rst,
    output reg data_out
);

reg [7:0] counter;

always @(posedge clk or posedge rst) begin
    if (rst) begin
        counter <= 8'b0;
        data_out <= 0;
    end else begin
        counter <= counter + 1;
        data_out <= counter[0];  // Simple data stream using LSB of counter
    end
end

endmodule
