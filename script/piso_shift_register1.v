module piso_shift_register (
input  clk,
input  enable,
input  reset,
output  [7:0]shift_reg,
input  load, // Control signal to load parallel data
input  [7:0] parallel_in, // 8-bit parallel input
output  serial_out // Serial output
);
	reg [7:0] shift_reg1;
 
	always @(posedge clk ) begin
		if (reset) begin
			shift_reg1 <= 8'b0;
		end
		else if (enable) begin
			if (load) begin
			shift_reg1 <= parallel_in;
			end else begin
			shift_reg1 <= {shift_reg1[6:0], 1'b0}; // Shift left and insert a 0 at LSB
			end
		end
		end
	 
	assign serial_out = shift_reg1[7]; // MSB is the serial output
	assign shift_reg =shift_reg1; 
	
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(1, piso_shift_register);
  end
endmodule