module counter_tb;

reg clk;
reg rst;
wire [3:0] count;

counter uut (
    .clk(clk),
    .rst(rst),
    .count(count)
);

initial begin
    clk = 0;
    rst = 1;
    #5 rst = 0;
end

always #5 clk = ~clk;

initial begin
    #100 
    $finish;
end

endmodule
