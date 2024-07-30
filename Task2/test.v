module test (clock1,clock2,rst,enable,next,data_in,decre_in,data_out);
input clock1; //250 Mhz clock input
input clock2; //100Mhz clock input
input rst; //active high reset input
input enable ; // enable input
input next; 
input [3:0] data_in; // incremental data input
input [3:0] decre_in; // decremental data input
output reg [3:0] data_out; //output data
 
always @ (posedge clock1) 
	begin
		if (rst == 1) 
			data_out <= 0;
		else 
			begin
			if (enable == 1) 
				data_out <= data_in;
			else 
				data_out <= data_out;
			end
	end
endmodule
