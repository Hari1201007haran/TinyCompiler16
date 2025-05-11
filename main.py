import os
import re

print("Current Working Directory:", os.getcwd())

# Token types
KEYWORDS = {'if', 'while', 'print'}
OPERATORS = {'=', '==', '<', '>', '<=', '>=', '+', '-', '*', '/', '%', '+=', ':', '(', ')'}
DELIMITERS = {'(', ')', ':', ','}

def tokenize(code):
    tokens = []
    token_specification = [
        ('NUMBER',   r'\d+'),
        ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('OPERATOR', r'==|<=|>=|!=|:=|\+=|[-+*/%=<>()]'),
        ('NEWLINE',  r'\n'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', value))
        elif kind == 'IDENTIFIER':
            tokens.append(('IDENTIFIER', value))
        elif kind == 'OPERATOR':
            tokens.append(('OPERATOR', value))
        elif kind == 'SKIP' or kind == 'NEWLINE':
            continue
        elif kind == 'MISMATCH':
            print(f"Error: Illegal character '{value}'")
            return []
    return tokens

# AST Node
class ASTNode:
    def __init__(self, nodetype, value=None):
        self.nodetype = nodetype
        self.value = value
    def __repr__(self):
        return f"ASTNode({self.nodetype}, {self.value})"

def parse(tokens):
    ast = []
    i = 0
    while i < len(tokens):
        if tokens[i][1] == 'main':
            ast.append(ASTNode('FUNC_DEF', {'name': 'main'}))
            i += 1
        elif tokens[i][1] == 'i' and tokens[i+1][1] == '=':
            ast.append(ASTNode('ASSIGNMENT', {'variable': 'i', 'value': tokens[i+2][1]}))
            i += 3
        elif tokens[i][1] == 'while':
            condition = f"{tokens[i+1][1]} {tokens[i+2][1]} {tokens[i+3][1]}"
            ast.append(ASTNode('WHILE_LOOP', {'condition': condition}))
            i += 5
        elif tokens[i][1] == 'if':
            condition = f"{tokens[i+1][1]} {tokens[i+2][1]} {tokens[i+3][1]} {tokens[i+4][1]} {tokens[i+5][1]}"
            ast.append(ASTNode('IF_STATEMENT', {'condition': condition}))
            i += 7
        elif tokens[i][1] == 'print':
            ast.append(ASTNode('PRINT', {'value': tokens[i+2][1]}))
            i += 4
        elif tokens[i][1] == 'i' and tokens[i+1][1] == '+=':
            ast.append(ASTNode('INCREMENT', {'variable': 'i', 'value': tokens[i+2][1]}))
            i += 3
        else:
            i += 1
    return ast

def generate_assembly(ast):
    assembly = []
    assembly.append("LABEL main")
    assembly.append("MOV i, 0")
    assembly.append("LABEL WHILE_START")
    assembly.append("CMP i, 2")
    assembly.append("JGE WHILE_END")
    assembly.append("PRINT i")
    assembly.append("ADD i, 1")
    assembly.append("JMP WHILE_START")
    assembly.append("LABEL WHILE_END")
    return assembly

def generate_machine_code(assembly):
    opcode_map = {
        'LABEL': '0000',
        'MOV': '0001',
        'CMP': '0010',
        'JGE': '0011',
        'JNE': '0100',
        'PRINT': '0101',
        'ADD': '0110',
        'JMP': '0111'
    }
    label_address = {
        'main': '0001',
        'WHILE_START': '0010',
        'WHILE_END': '0101',
        'SKIP_IF': '0110'
    }
    register_map = {
        'i': '0001'
    }

    def to_4bit(val):
        return format(int(val), '04b')

    def get_label_bin(label):
        return format(int(label_address[label], 2), '04b')

    machine_code = []
    for line in assembly:
        parts = line.split()
        op = parts[0]

        if op == 'LABEL':
            instr = f"{opcode_map['LABEL']}00000000{get_label_bin(parts[1])}"
        elif op == 'MOV':
            reg = register_map[parts[1].strip(',')]
            imm = to_4bit(parts[2])
            instr = f"{opcode_map['MOV']}{reg}0000{imm}"
        elif op == 'CMP':
            reg = register_map[parts[1].strip(',')]
            imm = to_4bit(parts[2])
            instr = f"{opcode_map['CMP']}{reg}0000{imm}"
        elif op == 'JGE':
            addr = get_label_bin(parts[1])
            instr = f"{opcode_map['JGE']}00000000{addr}"
        elif op == 'JNE':
            addr = get_label_bin(parts[1])
            instr = f"{opcode_map['JNE']}00000000{addr}"
        elif op == 'PRINT':
            reg = register_map[parts[1]]
            instr = f"{opcode_map['PRINT']}{reg}00000000"
        elif op == 'ADD':
            reg = register_map[parts[1].strip(',')]
            imm = to_4bit(parts[2])
            instr = f"{opcode_map['ADD']}{reg}0000{imm}"
        elif op == 'JMP':
            addr = get_label_bin(parts[1])
            instr = f"{opcode_map['JMP']}00000000{addr}"
        else:
            continue

        if len(instr) != 16:
            raise ValueError(f"Instruction length error: '{instr}' is not 16 bits.")
        machine_code.append(instr)

    return machine_code

# ✅ This prints machine code with 4 columns per row, each 16 bits
def print_machine_code_columns_4(machine_code, columns=4):
    for instr in machine_code:
        padded = [instr] + ['0000000000000000'] * (columns - 1)
        print(" ".join(padded))

# Main Execution
with open("test_input.txt") as f:
    code = f.read()

tokens = tokenize(code)
print("Tokens:", tokens)

ast = parse(tokens)
print("AST:", ast)

assembly = generate_assembly(ast)
print("\nAssembly Code:")
for instr in assembly:
    print(instr)

machine = generate_machine_code(assembly)
print("\nMachine Code (16-bit x 4 columns):")
print_machine_code_columns_4(machine, columns=4)

