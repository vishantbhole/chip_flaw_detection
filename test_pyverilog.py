from pyverilog.vparser.parser import parse
with open('dataset/design.v', 'r') as f:
    code = f.read()
ast, directives = parse([code])
print(ast)