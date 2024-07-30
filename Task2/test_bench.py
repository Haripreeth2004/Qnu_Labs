import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse
import re
import random

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
    
    # Extract signals from the portlist
    for port in module.portlist.ports:
        if isinstance(port, vast.Ioport):
            if isinstance(port.first, vast.Input):
                name = port.first.name
                width = get_width(port.first)
                inputs.append((name, width))
            elif isinstance(port.first, vast.Output):
                name = port.first.name
                width = get_width(port.first)
                outputs.append((name, width))
    
    # Extract signals from the internal declarations
    for item in module.items:
        if isinstance(item, vast.Decl):
            for decl in item.list:
                if isinstance(decl, vast.Input):
                    name = decl.name
                    width = get_width(decl)
                    inputs.append((name, width))
                elif isinstance(decl, vast.Output):
                    name = decl.name
                    width = get_width(decl)
                    outputs.append((name, width))

    # Extract signals from outside the module declarations
    for item in ast.description.definitions:
        if isinstance(item, vast.Decl):
            for decl in item.list:
                if isinstance(decl, vast.Input):
                    name = decl.name
                    width = get_width(decl)
                    inputs.append((name, width))
                elif isinstance(decl, vast.Output):
                    name = decl.name
                    width = get_width(decl)
                    outputs.append((name, width))
    
    return inputs, outputs 

def get_width(signal):
    if signal.width:
        msb = int(signal.width.msb.value)
        lsb = int(signal.width.lsb.value)
        width = msb - lsb + 1
    else:
        width = 1  # Default width is 1 bit
    return width
def generate_random_value(width): #num_format
    value = random.randint(0, (1 << width) - 1)
    ### IF YOU WANT NUM_FORMAT Uncomment this and add the num_format at required function arguments
    """if num_format == "hex":
        return hex(value)
    elif num_format == "bin":
        return bin(value)              
    elif num_format == "oct":
        return oct(value)
    else:  # Default is decimal
        return str(value)"""
    return value
    
    
"""def get_number_format():
    print("Choose number format for random data values:")
    print("1. Decimal")
    print("2. Hexadecimal")
    print("3. Binary")
    print("4. Octal")
    choice = input("Enter your choice (1/2/3/4): ")
    if choice == '1':
        return "dec"
    elif choice == '2':
        return "hex"
    elif choice == '3':
        return "bin"
    elif choice == '4':
        return "oct"
    else:
        print("Invalid choice. Defaulting to Decimal.")
        return "dec"   """

def generate_testbench(module, inputs, outputs, clock_info, reset_info, reset_order, data_info, data_order):#num_format
    module_name = module.name
    tb_filename = f'{module_name}_tb.v'

    # Create the input and output declarations
    input_declarations = "\n    ".join(f"reg {'[{}:0] '.format(width-1) if width > 1 else ''}{signal};" for signal, width in inputs)
    output_declarations = "\n    ".join(f"wire {'[{}:0] '.format(width-1) if width > 1 else ''}{signal};" for signal, width in outputs)

    # Create the port connections
    port_connections = ",\n        ".join(f".{signal}({signal})" for signal, _ in inputs + outputs)

    # Clock Generation
    clock_generation = ""
    for signal, freq in clock_info.items():
        time_period = 1 / freq * 1e9
        clock_generation += f"    always #({time_period}) {signal} = ~{signal};\n"

    # Reset Initialization and Toggling
    reset_initialization = generate_reset_initialization(inputs, reset_order, reset_info, data_info, data_order)
    
    # Data Initialization
    data_initialization = generate_data_initialization(data_order, inputs, data_info)#num_format
    ID_data_initialization = generate_ID_data_initialization(data_order, inputs, data_info)

    # Define the template for the testbench
    tb_template = f"""
module {module_name}_tb;
    
    // Inputs
    {input_declarations}

    // Outputs
    {output_declarations}

    // Instantiate DUT (Design Under Test)
    {module_name} dut (
        {port_connections}
    );

    // Initial Block
    initial begin
    // VCD Dump commands
    $dumpfile("test_tb.vcd");  // Specify the name of the VCD file
    $dumpvars(0, test_tb);  // Dump variables from the testbench module
{reset_initialization}
{data_initialization}
        #100;  // Simulation end time
        $finish;
    end
    // always block initialisation
{ID_data_initialization}
    
    // Clock Generation
{clock_generation}

endmodule
"""
    return tb_template,tb_filename

def generate_reset_initialization(inputs, reset_order, reset_info, data_info, data_order):
    initializations = []
    reset_initializations = []

    input_signals = {signal for signal, _ in inputs}
    reset_signals_done = set()

    # First initialize all input signals to 0 except reset and data signals
    for signal, _ in inputs:
        if signal not in reset_info and signal not in data_info:
            initializations.append(f"        {signal} = 0;")

    # Handle reset signals based on their active state
    for reset_signal in reset_order:
        if reset_signal in input_signals and reset_signal not in reset_signals_done:
            if reset_info[reset_signal] == 'active low':
                reset_initializations.append(f"        {reset_signal} = 0;")
                reset_initializations.append(f"        #10 {reset_signal} = 1;")
            else:  # active high
                reset_initializations.append(f"        {reset_signal} = 1;")
                reset_initializations.append(f"        #10 {reset_signal} = 0;")
            reset_signals_done.add(reset_signal)

    return "\n".join(initializations + reset_initializations)


def generate_data_initialization(data_order, inputs, data_info): # num_format
    data_initializations = []
    data_signals_done = set()

    # Create a dictionary to map signal names to their widths
    input_signals = {signal.split()[0]: int(width) for signal, width in inputs}

    # Handle data signals
    for data_signal in data_order:
        clean_data_signal = re.sub(r'\[\d+:\d+\]', '', data_signal).strip()  # Remove [7:0] if present
        if clean_data_signal in input_signals and clean_data_signal not in data_signals_done:
            width = input_signals[clean_data_signal]  # Get the width of the signal
            random_value = generate_random_value(width) #num_format, # Generate initial random value based on width
            data_initializations.append(f"        {clean_data_signal} = {random_value};")
            
            if data_signal in data_info:
                if data_info[data_signal] == 'random data':
                    for _ in range(3):  # Generate random value initialization three times
                        random_value = generate_random_value(width)#num_format
                        data_initializations.append(f"        #10 {clean_data_signal} = {random_value};")
                data_signals_done.add(clean_data_signal)

    return "\n".join(data_initializations)
def generate_ID_data_initialization(data_order, inputs, data_info): # num_format
    ID_data_initializations = []
    data_signals_done = set()

    # Create a dictionary to map signal names to their widths
    input_signals = {signal.split()[0]: int(width) for signal, width in inputs}

    # Handle data signals
    for data_signal in data_order:
        clean_data_signal = re.sub(r'\[\d+:\d+\]', '', data_signal).strip()  # Remove [7:0] if present
        if clean_data_signal in input_signals and clean_data_signal not in data_signals_done:
            width = input_signals[clean_data_signal]  # Get the width of the signal
            #random_value = generate_random_value(width) #num_format, # Generate initial random value based on width
            
            #ID_data_initializations.append(f"        {clean_data_signal} = {random_value};")
            
            if data_signal in data_info:
                if data_info[data_signal] == 'incremental data':
                    ID_data_initializations.append(
                        f"    always #10 begin if ( {clean_data_signal} > 3) begin {clean_data_signal} = {clean_data_signal} + 1; end end") #You can change the condition as per wish in if condition 
                elif data_info[data_signal] == 'decremental data':
                    ID_data_initializations.append(
                        f"    always #10 begin if ({clean_data_signal} > 0) begin {clean_data_signal} = {clean_data_signal} - 1; end end")  #You can change the condition as per wish in if condition 
    return "\n".join(ID_data_initializations)

def save_testbench(tb_content, tb_filename):
    with open(tb_filename, 'w') as tb_file:
        tb_file.write(tb_content)

def extract_comments_and_keywords(verilog_file):
    comments = []
    keywords = ["input", "output", "reset", "clock", "active high", "active low", "data", "random", "incremental","decremental"]
    keyword_comments = {key: [] for key in keywords}
    clock_info = {}
    reset_info = {}
    reset_order = []
    data_info = {}
    data_order = []
    
    with open(verilog_file, 'r') as file:
        for line in file:
            comment_match = re.search(r'//.*|/\*.*?\*/', line)
            if comment_match:
                comment = comment_match.group()
                comments.append(comment)
                for keyword in keywords:
                    if re.search(rf'\b{keyword}\b', comment, re.IGNORECASE):
                        keyword_comments[keyword].append(comment)
                        # Extract clock frequency and reset type information
                        if keyword == "clock":
                            clock_freq = extract_clock_frequency(comment)
                            if clock_freq:
                                signal_name = get_signal_from_comment(line)
                                if signal_name:
                                    clock_info[signal_name] = clock_freq
                        elif keyword == "reset" or keyword == "active high" or keyword == "active low":
                            reset_type = extract_reset_type(comment)
                            if reset_type:
                                reset_signal = get_signal_from_comment(line)
                                reset_info[reset_signal] = reset_type
                                if reset_signal not in reset_order:
                                    reset_order.append(reset_signal)
                        elif keyword == "data" or keyword == "random" or keyword == "incremental" or keyword == "decremental":
                            data_type = extract_data_type(comment)
                            if data_type:
                                data_signal = get_signal_from_comment(line)
                                if data_signal:
                                    data_info[data_signal] = data_type
                                    if data_signal not in data_order:
                                        data_order.append(data_signal)
    
    return comments, keyword_comments, clock_info, reset_info, reset_order, data_info, data_order

def extract_clock_frequency(comment):
    freq_match = re.search(r'(\d+)\s*(MHz|kHz)', comment, re.IGNORECASE)
    if freq_match:
        if freq_match.group(2).lower() == 'mhz':
            return float(freq_match.group(1)) * 1_000_000
        elif freq_match.group(2).lower() == 'khz':
            return float(freq_match.group(1)) * 1_000
    return None

def get_signal_from_comment(line):
    signal_match = re.search(r'input\s+(\[\d+:\d+\])?\s*(\w+)', line)
    if signal_match:
        if signal_match.group(1):  # If width is specified
            width = signal_match.group(1)
            signal_name = signal_match.group(2)
            return f"{signal_name} {width}"
        else:
            return signal_match.group(2)
    return None

def extract_reset_type(comment):
    if "active low" in comment.lower():
        return "active low"
    elif "active high" in comment.lower():
        return "active high"
    return None

def extract_data_type(comment):
    if "incremental" in comment.lower():
        return "incremental data"
    elif "random" in comment.lower():
        return "random data"
    elif "decremental" in comment.lower():
        return "decremental data"
    return None

def save_extracted_info(inputs, outputs, comments, keyword_comments, clock_info, reset_info, reset_order, data_info, data_order, filename):
    with open(filename, 'w') as file:
        file.write("Inputs:\n")
        for signal, width in inputs:
            file.write(f"{signal} [{width} bits]\n")
        
        file.write("\nOutputs:\n")
        for signal, width in outputs:
            file.write(f"{signal} [{width} bits]\n")
        
        file.write("\nComments:\n")
        file.write("\n".join(comments))
        
        for key, comments_list in keyword_comments.items():
            file.write(f"\n\n{key.capitalize()} Comments:\n")
            file.write("\n".join(comments_list))
        
        file.write("\n\nClock Information:\n")
        for signal, freq in clock_info.items():
            file.write(f"{signal}: {freq} Hz\n")
        
        file.write("\nReset Information:\n")
        for signal, reset_type in reset_info.items():
            file.write(f"{signal}: {reset_type}\n")
        
        file.write("\nReset Order:\n")
        for signal in reset_order:
            file.write(f"{signal}\n")
        
        if data_info:
            file.write("\nData Information:\n")
            for signal, data_type in data_info.items():
                file.write(f"{signal}: {data_type}\n")
        
        file.write("\nData Order:\n")
        for signal in data_order:
            file.write(f"{signal}\n")


if __name__ == "__main__":
    verilog_file = 'test.v'
    print(f"Verilog file path: {verilog_file}")
    #tb_filename = 'generated_testbench_tb.v'
    extracted_info_filename = 'extracted_info.txt'
    
    ast = parse_verilog(verilog_file)
    modules = get_module_info(ast)
    #num_format = get_number_format()
    
    all_inputs = []
    all_outputs = []
    all_comments = []
    all_keyword_comments = {key: [] for key in ["input", "output", "reset", "clock", "active high", "active low", "data", "random", "incremental","decremental"]}
    all_clock_info = {}
    all_reset_info = {}
    all_reset_order = []
    all_data_info = {}
    all_data_order = []

    for module in modules:
        inputs, outputs = extract_signals(module)
        comments, keyword_comments, clock_info, reset_info, reset_order, data_info, data_order = extract_comments_and_keywords(verilog_file)
        tb_content,tb_filename = generate_testbench(module, inputs, outputs, clock_info, reset_info, reset_order, data_info, data_order,)#num_format
        save_testbench(tb_content, tb_filename)
        
        all_inputs.extend(inputs)
        all_outputs.extend(outputs)
        all_comments.extend(comments)
        for key, value in keyword_comments.items():
            all_keyword_comments[key].extend(value)
        all_clock_info.update(clock_info)
        all_reset_info.update(reset_info)
        all_reset_order.extend(reset_order)
        all_data_info.update(data_info)
        all_data_order.extend(data_order)
        
        print(f"Testbench for module {module.name} saved to {tb_filename}")
    
    save_extracted_info(all_inputs, all_outputs, all_comments, all_keyword_comments, all_clock_info, all_reset_info, all_reset_order, all_data_info, all_data_order, extracted_info_filename)
    print(f"Extracted information saved to {extracted_info_filename}")
