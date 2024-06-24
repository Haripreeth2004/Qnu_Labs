// File: jc2_alt.v
// Generated by MyHDL 0.11.46
// Date: Thu Jun 13 14:42:07 2024


`timescale 1ns/10ps

module jc2_alt (
    goLeft,
    goRight,
    stop,
    clk,
    q
);
// A bi-directional 4-bit Johnson counter with stop control.
// 
// I/O pins:
// --------
// 
// clk      : input free-running clock 
// goLeft   : input signal to shift left (active-low switch)
// goRight  : input signal to shift right (active-low switch)
// stop     : input signal to stop counting (active-low switch)
// q        : 4-bit counter output (active-low LEDs; q[0] is right-most)

input goLeft;
input goRight;
input stop;
input clk;
output [3:0] q;
reg [3:0] q;




always @(posedge clk) begin: JC2_ALT_LOGIC
    reg [1-1:0] dir;
    reg run;
    if ((goRight == 0)) begin
        dir = 1'b0;
        run = 1'b1;
    end
    else if ((goLeft == 0)) begin
        dir = 1'b1;
        run = 1'b1;
    end
    if ((stop == 0)) begin
        run = 1'b0;
    end
    if (run) begin
        if ((dir == 1'b1)) begin
            q[4-1:1] <= q[3-1:0];
            q[0] <= (!q[3]);
        end
        else begin
            q[3-1:0] <= q[4-1:1];
            q[3] <= (!q[0]);
        end
    end
end

endmodule
