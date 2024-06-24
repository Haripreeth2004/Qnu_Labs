from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

# Path to the Verilog file
verilog_file = '/workspaces/Qnu_Labs/JC_new/tb_jc2_alt.v'

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

# Create a visitor and visit the parsed AST
visitor = VerilogVisitor(ast)
visitor.visit(ast)
# Save output to a text file
output_file = 'jc_new_ast_output.txt'

with open(output_file, 'w') as file:
    file.write("Modules found:\n")
    for module in visitor.modules:
        file.write(module + '\n')
    
    file.write("\nSignals found:\n")
    for signal_type, signal_name in visitor.signals:
        file.write(f"{signal_type}: {signal_name}\n")

print(f"Output saved to {output_file}")
# Print extracted information
print("Modules found:", visitor.modules)
print("Signals found:", visitor.signals)
