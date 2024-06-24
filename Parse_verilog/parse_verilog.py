from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

# Path to the Verilog file
verilog_file = '/workspaces/Qnu_Labs/Parse_verilog/piso_shift_register.v'

# Parse the Verilog file
ast, directives = parse([verilog_file])

# Generate and print AST code
codegen = ASTCodeGenerator()
generated_code = codegen.visit(ast)
print("Generated AST Code:\n", generated_code)

# Custom Visitor Class
class VerilogVisitor(object):
    def __init__(self, ast):
        self.ast = ast
        self.modules = []
        self.signals = []

    def visit_ModuleDef(self, node):
        self.modules.append(node.name)
        for item in node.children():
            self.visit(item)

    def visit_Input(self, node):
        self.signals.append(('input', node.name))

    def visit_Output(self, node):
        self.signals.append(('output', node.name))

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for item in node.children():
            self.visit(item)

# Function to write data to a file
def write_data_to_file(modules, signals, filename):
    with open(filename, 'w') as f:
        f.write("Modules found:\n")
        for module in modules:
            f.write(f"{module}\n")
        f.write("\nSignals found:\n")
        for signal in signals:
            f.write(f"{signal[0]}: {signal[1]}\n")

# Create a visitor and visit the parsed AST
visitor = VerilogVisitor(ast)
visitor.visit(ast)

# Print extracted information
print("Modules found:", visitor.modules)
print("Signals found:", visitor.signals)

# Store extracted information in a file
output_file = '/workspaces/Qnu_Labs/Parse_verilog/extracted_data.txt'
write_data_to_file(visitor.modules, visitor.signals, output_file)
