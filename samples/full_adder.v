// full_adder.v
module full_adder (
    input A,
    input B,
    input Cin,
    output Sum,
    output Cout
);

wire Sum1, Carry1, Carry2;

half_adder HA1(.A(A), .B(B), .Sum(Sum1), .Carry(Carry1));
half_adder HA2(.A(Sum1), .B(Cin), .Sum(Sum), .Carry(Carry2));
assign Cout = Carry1 | Carry2;

endmodule

initial begin
            $dumpfile("dump.vcd");
            $dumpvars(0,full_adder);
        end
        