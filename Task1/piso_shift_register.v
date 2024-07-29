module piso_shift_register (
input  clock,// input clock 5MHZ
input clk1, //input clock 20Mhz
input clk2, //input clock 10Mhz
input  enable,// input enable
input  reset, // active low input reset
input rstn, // active high input reset
output reg [7:0]shift_reg, // output
input  load, // Control signal to load parallel input 
input  [7:0] parallel_in, // 8-bit parallel incremental input 
input  [3:0] serial_in, // 4-bit serial incremental input 
input  [3:0] decre_in, // 8 bit decremental input 
input  [7:0] data1, // 8-bit random input data
input [15:0] High_data, // 16 bit random input data
input data2, // random input data
input reset1,// active high input
output reg  serial_out // Serial output
);
	
	always @(posedge clk1 ) begin
		if (reset || !enable) begin
			shift_reg <= 8'b0;
			serial_out <= 1'b0;
		end
		else if (enable) begin
			if (load) begin
			shift_reg <= parallel_in; // output shift_reg
			end else begin
			shift_reg <= {shift_reg[6:0], 1'b0}; // Shift left and insert a 0 at LSB
			serial_out = shift_reg[7]; // MSB is the serial output
			end
		end
		end
endmodule
