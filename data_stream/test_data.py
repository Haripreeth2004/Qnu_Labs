import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse

def parse_verilog(verilog_file):
    ast, directives = parse([verilog_file])
    return ast

def get_module_info(ast):
    modules = []
    for item in ast.description.definitions:
        if isinstance(item, vast.ModuleDef):
            modules.append(item)
    return modules

def extract_signals(module):
    inputs = []
    outputs = []
    for port in module.portlist.ports:
        if isinstance(port, vast.Ioport):
            port_name = port.first.name
            width = 1  # Default width is 1 bit
            if port.first.width:
                msb = int(port.first.width.msb.value)
                lsb = int(port.first.width.lsb.value)
                width = msb - lsb + 1

            if isinstance(port.first, vast.Input):
                inputs.append((port_name, width))
            elif isinstance(port.first, vast.Output):
                outputs.append((port_name, width))
    return inputs, outputs

def generate_testbench(module, inputs, outputs):
    module_name = module.name

    # Create the input and output declarations
    input_declarations = "\n    ".join(f"reg {'[{}:0] '.format(width-1) if width > 1 else ''}{signal};" for signal, width in inputs)
    output_declarations = "\n    ".join(f"wire {'[{}:0] '.format(width-1) if width > 1 else ''}{signal};" for signal, width in outputs)

    # Create the port connections
    connected_signals = set()
    port_connections = []
    for signal, width in inputs + outputs:
        if signal not in connected_signals:
            port_connections.append(f".{signal}({signal})")
            connected_signals.add(signal)
    
    port_connections_str = ",\n        ".join(port_connections)

    # Generate test vectors (toggle each non-clock input signal once for demonstration)
    test_vectors = ""
    toggle_time = 10  # Time interval for toggling signals
    for _ in range(3):  # Three iterations
        for signal, _ in inputs:
            if signal != 'clk':  # Exclude 'clk' from test vectors
                test_vectors += f"        #{toggle_time} {signal} = ~{signal};\n"
        test_vectors += "\n\n"  # Add space (new line) between each iteration

    # Define the template for the testbench
    tb_template = f"""
module {module_name}_tb;

    // Inputs
    {input_declarations}

    // Outputs
    {output_declarations}

    // Instantiate DUT (Design Under Test)
    {module_name} dut (
        {port_connections_str}
    );

    // Initial Block
    initial begin
        clk = 0;
{test_vectors}
        #100;  // Simulation end time
        $finish;
    end

    // Clock Generation
    always #5 clk = ~clk;

endmodule
"""
    return tb_template

def save_testbench(tb_content, tb_filename):
    with open(tb_filename, 'w') as tb_file:
        tb_file.write(tb_content)

def save_signals(inputs, outputs, filename):
    with open(filename, 'w') as sig_file:
        sig_file.write("Inputs:\n")
        for signal, width in inputs:
            sig_file.write(f"{signal} [{width} bits]\n")
        sig_file.write("\nOutputs:\n")
        for signal, width in outputs:
            sig_file.write(f"{signal} [{width} bits]\n")

if __name__ == "__main__":
    verilog_file = '/workspaces/Qnu_Labs/data_stream/data_stream.v'  # Update this path to your Verilog file
    tb_filename = 'generated_testbench_tb.v'
    sig_filename = 'extracted_signals.txt'
    
    ast = parse_verilog(verilog_file)
    modules = get_module_info(ast)
    
    for module in modules:
        inputs, outputs = extract_signals(module)
        tb_content = generate_testbench(module, inputs, outputs)
        save_testbench(tb_content, tb_filename)
        save_signals(inputs, outputs, sig_filename)
        print(f"Testbench for module {module.name} saved to {tb_filename}")
        print(f"Signals saved to {sig_filename}")
