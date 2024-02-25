# Copyright (C) 2024  Felipe Bombardelli <felipebombardelli@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ============================================================================
#  Header
# ============================================================================

# https://pypi.org/project/ply/

import ply.lex as lex
import ply.yacc as yacc
import numpy as np
import json
import ufr

# ============================================================================
#  Computador
# ============================================================================

class Computer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.code = np.zeros(256, dtype=np.uint8)
        self.registers = {"ax": 10, "bx": 20, "cx": 30, "dx": 40, "sx": 0}
        self.memory = np.zeros(256, dtype=np.uint8)
        self.input = {"teclado": "felipe"}
        self.alu = {"op": "+", "op1": 0, "op2": 0, "res": 0, "dst": ""}

    def alu_exec(self, op: str, op1: int, op2: int, dst: str, dst_idx):
        # execute
        if op == '+':
            res = op1 + op2
        elif op == '-':
            res = op1 - op2
        elif op == '*':
            res = op1 * op2
        elif op == '/':
            res = op1 / op2

        # save the values
        self.alu['op'] = op
        self.alu['op1'] = op1
        self.alu['op2'] = op2
        self.alu['res'] = res

        # store the result
        try:
            if dst == 'memory':
                if res < 256:
                    self.memory[dst_idx] = res
                elif res < 65536:
                    self.memory[dst_idx] = res & 0xFF
                    self.memory[dst_idx+1] = (res >> 8) & 0xFF

                self.alu['dst'] = f"{dst}[{dst_idx}]"
            elif dst == 'register':
                self.registers[dst_idx] = res
                self.alu['dst'] = f"{dst_idx}"
        except:
            g_error = "Error na execucao da instrucao"

    # mov
    def mov_num2reg(self, num: int, reg_name: str):
        self.alu_exec('+', num, 0, 'register', reg_name)

    def mov_num2mem(self, num: int, mem_idx: int):
        self.alu_exec('+', num, 0, 'memory', mem_idx)

    def mov_reg2reg(self, reg_src: str, reg_dst: str):
        self.alu_exec('+', self.registers[reg_src], 0, 'register', reg_dst)

    def mov_reg2mem(self, reg_src: str, mem_idx: int):
        self.alu_exec('+', self.registers[reg_src], 0, 'memory', mem_idx)

    def mov_inp2reg(self, input_name: str, reg_dst: str):
        try:
            device = self.input[input_name]
            byte = device[0]
            self.registers[reg_dst] = ord(byte)
            self.input[input_name] = device[1:]
        except:
            self.registers[reg_dst] = 0

    # adi
    def adi_num2reg(self, num: int, reg: str):
        self.alu_exec('+', self.registers[reg], num, 'register', reg)

    # sub
    def sub_num2reg(self, num: int, reg: str):
        self.alu_exec('-', self.registers[reg], num, 'register', reg)

    # show
    def __str__(self):
        text = json.dumps({
            "registers": self.registers
            , "memory": self.memory.tolist()
            , "input": self.input
            , 'alu': self.alu
            # , "code": self.code.tolist()
        })
        return text

g_computer = Computer()
g_error = ""

# ============================================================================
#  Lex
# ============================================================================

tokens = (
    'NUMERO', 'MOVA', 'PARA', 'REGISTRADOR', 'ADICIONE', 'SUBTRAIA', 'SE',
    'ENTAO', 'MEMORIA', 'LEIA', 'TECLADO'
)
# leia, escreva, empurre, puxe, chame

literals = ['=', '+', '-', '*', '/', '(', ')', '[', ']']

# Tokens
t_ignore = " \t"
t_MOVA = 'mova'
t_PARA = 'para'
t_SE = 'se'
t_ENTAO = 'entao'
t_LEIA = 'leia'

# def t_MOVA(t):
#    'mova'
#    return t

def t_ADICIONE(t):
    'adicione'
    return t

def t_SUBTRAIA(t):
    'subtraia'
    return t

def t_MEMORIA(t):
    'memoria'
    return t

def t_REGISTRADOR(t):
    r'[abcd]x'
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_TECLADO(t):
    r'teclado'
    return t

# t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

# ============================================================================
#  Parser
# ============================================================================

# Parsing rules
precedence = (
    # ('left', '+', '-'),
    # ('left', '*', '/')
)

# dictionary of names
names = {}

def p_mova_num2reg(p):
    'statement : MOVA NUMERO PARA REGISTRADOR'
    g_computer.mov_num2reg(p[2], p[4])

# Register to *
def p_mova_reg2reg(p):
    'statement : MOVA REGISTRADOR PARA REGISTRADOR'
    g_computer.mov_reg2reg(p[2], p[4])

def p_mova_reg2mem(p):
    'statement : MOVA REGISTRADOR PARA MEMORIA "[" NUMERO "]"'
    g_computer.mov_reg2mem(p[2], p[6])

# Numero to *
def p_mova_num2mem(p):
    'statement : MOVA NUMERO PARA MEMORIA "[" NUMERO "]" '
    g_computer.mov_num2mem(p[2], p[6])

def p_adicione_num2reg(p):
    'statement : ADICIONE NUMERO PARA REGISTRADOR'
    g_computer.adi_num2reg(p[2], p[4])

def p_subtraia_num2reg(p):
   'statement : SUBTRAIA NUMERO PARA REGISTRADOR'
   g_computer.sub_num2reg(p[2], p[4])

def p_leia(p):
   'statement : LEIA TECLADO PARA REGISTRADOR'
   g_computer.mov_inp2reg(p[2], p[4])

def p_se_entao(p):
   'statement : SE NUMERO ENTAO'
   # g_computer.sub_num2reg(p[4], p[2])
   print("opa")

def p_error(p):
    global g_error
    if p:
        g_error = "Syntax error at '%s'" % p.value
        print(g_error)
    else:
        g_error = "Syntax error at EOF"
        print(g_error)

# ============================================================================
#  Main
# ============================================================================

lexer = lex.lex()
parser = yacc.yacc()

sock = ufr.Server("@new zmq:socket @port 4000 @coder msgpack:obj") 

while True:
    sock.recv()
    command = sock.get("s")
    if command == "get_data":
        sock.putln( "OK", str(g_computer) )
    elif command == "exec":
        g_error = ""
        instruction = sock.get("s")
        yacc.parse(instruction)
        if g_error != "":
            sock.putln("ERROR", g_error)
        else:
            sock.putln("OK")
    else:
        sock.putln("ERROR")

# ============================================================================
#  Tests
# ============================================================================

def test():
    yacc.parse("mova 10 para ax")
    yacc.parse("mova ax para bx")
    yacc.parse("mova 14 para memoria[10]")
    yacc.parse("adicione 23 para bx")
    yacc.parse("subtraia 23 para bx")
    yacc.parse("se 20 entao")

