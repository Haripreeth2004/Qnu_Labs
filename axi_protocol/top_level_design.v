module axistream (
    input axi_clk,
    input s_axis_tvalid,
    output reg s_axis_tready,
    input s_axis_tlast,
    input [31:0] s_axis_tdata,
    output reg m_axis_tvalid,
    input m_axis_tready,
    output reg m_axis_tlast,
    output reg [31:0] m_axis_tdata
);

    // Assign s_axis_tready based on m_axis_tready
    assign s_axis_tready = m_axis_tready;

    // Process for driving m_axis_tdata and m_axis_tlast
    always @ (posedge axi_clk) begin
        if (s_axis_tvalid & s_axis_tready) begin
            m_axis_tdata <= s_axis_tdata;
            m_axis_tlast <= s_axis_tlast;
        end else begin
            m_axis_tdata <= 'h0;
            m_axis_tlast <= 1'b0;
        end
    end

    // Assign m_axis_tvalid
    always @ (posedge axi_clk) begin
        m_axis_tvalid <= s_axis_tvalid & s_axis_tready;
    end

    // Initial block for dumping signals
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(1, axistream);
    end

endmodule
