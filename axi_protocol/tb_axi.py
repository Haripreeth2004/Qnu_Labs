import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotbext.axi import AxiStreamBus, AxiStreamSource, AxiStreamSink

@cocotb.test()
async def test_axistream_passthrough(dut):
    """ Test AXI Stream Master-Slave communication """
    clock = Clock(dut.axi_clk, 10, units="ns")
    cocotb.fork(clock.start())

    axi_source = AxiStreamSource(AxiStreamBus.from_prefix(dut, "s_axis"), dut.axi_clk)
    axi_sink = AxiStreamSink(AxiStreamBus.from_prefix(dut, "m_axis"), dut.axi_clk)

    # Reset signals
    dut.s_axis_tvalid <= 0
    dut.s_axis_tlast <= 0
    dut.m_axis_tready <= 0

    await Timer(10, units="ns")

    # Enable sink to accept data
    dut.m_axis_tready <= 1
    await Timer(20, units="ns")

    # Send data from source
    data = [0x01, 0x02, 0x03, 0x04, 0x05]
    await axi_source.send(data)

    # Wait for data to be received in sink
    await Timer(10, units="ns")
    received_data = await axi_sink.recv()

    # Print received data (for verification)
    print(f"Received data: {received_data}")

    # Add assertions as needed to verify the received data

