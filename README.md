# TinyCompiler16

**TinyCompiler16** is a lightweight educational compiler written in Python that converts a simple custom programming language into 16-bit machine code. It demonstrates the essential phases of a compiler: tokenization, parsing, AST construction, and code generation.

---

## 🔧 Features

- Lexical Analyzer (Tokenizer) using Python regular expressions
- Simple Parser that builds an Abstract Syntax Tree (AST)
- Assembly-like Intermediate Code Generation
- Machine Code Generator for a 16-bit instruction set
- Supports control flow: `if`, `while`, `print`, assignments

---

## 🚀 Example

### Input (`test_input.txt`)

```python
main
i = 0
while i < 2:
    print(i)
    i += 1
Output (16-bit machine code, 4 columns)

0000000000000001 0000000000000000 0000000000000000 0000000000000000
0001000100000000 0000000000000000 0000000000000000 0000000000000000
0010000100000010 0000000000000000 0000000000000000 0000000000000000
0011000000000101 0000000000000000 0000000000000000 0000000000000000
0101000100000000 0000000000000000 0000000000000000 0000000000000000
0110000100000001 0000000000000000 0000000000000000 0000000000000000
0111000000000010 0000000000000000 0000000000000000 0000000000000000
0000000000000101 0000000000000000 0000000000000000 0000000000000000

🧠 Concepts Covered
Compiler Design Fundamentals

Abstract Syntax Tree (AST)

Instruction Encoding & Binary Code

Python Scripting and Regex-based Tokenization

✅ Requirements
Python

Created by Hariharan

