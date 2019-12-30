#!/usr/bin/env python
"""
This is a Brainfuck interpreter (not a compiler) written in Python. It is
somewhat optimized for speed, as much as that is possible. By default it allows
for 30000 bytes of memory, but this can be configured by passing a parameter.
Some protections are in place in order to keep the program from entering an
infinite loop. There is no recursion in the interpreter, in order to avoid
stack overflows. It also contains a very rudementary debugger which, for each
opcode, prints the current position in the code and the contents of the memory.
"""

import sys
from io import StringIO
import numpy as np


class BrainfuckError(Exception):
    def __init__(self, message, errnr):
        self.errnr = errnr
        Exception.__init__(self, message)


class Brainfuck(object):
    """
    Brainfuck interpreter.
    Example:
            # Divide
            bf = brainfuck.Brainfuck(
                    \"""
                            ,>,>++++++[-<--------<-------->>]<<[>[->+>+<<
                            ]>[-<<-[>]>>>[<[>>>-<<<[-]]>>]<<]>>>+<<[-<<+>>
                            ]<<<]>[-]>>>>[-<<<<<+>>>>>]<<<<++++++[-<++++++++>]
                            <.
                    \""",
                    '62')
            out = bf.run()
            print out              # 3
    """

    operators = ['+', '-', '>', '<', '[', ']', '.', ',']

    def __init__(self, code, input=sys.stdin, output=None):
        """
        Interpret and run Brainfuck code given in 'code'. Brainfuck program
        will read from input which can be either an open filehandle (default
        stdin) or a string. Will write to output. If output is None (default),
        the run() function will return the output instead.
        """
        if isinstance(input, str):
            self.input = StringIO(input)
        else:
            self.input = input
        if output is None:
            self.return_output = True
            self.output = StringIO()
        else:
            self.return_output = False
            self.output = output

        # Syntax checking :-D
        if code.count('[') != code.count(']'):
            raise BrainfuckError('Unmatched number of brackets', 1)

        # Remove non-brainfuck operators so the interpreter doesn't have to
        # process them.
        c = ''
        for op in code:
            if op in self.operators:
                c += op
        code = c

        # Find matching brackets upfront so we don't have to do it many times
        # in the code.
        # Reference dict of brackets and their matching brackets
        self.jumps = {}
        self.c_len = len(code)  # Code length
        d_ip = 0               # Discover Instruction Pointer
        while d_ip < self.c_len:
            instr = code[d_ip]
            if instr == '[':
                # Scan for matching bracket forwards
                heap = 0
                for ip in range(d_ip+1, self.c_len):
                    if code[ip] == '[':
                        heap += 1
                    elif code[ip] == ']':
                        if heap == 0:
                            self.jumps[d_ip] = ip
                            break
                        else:
                            heap -= 1
                if d_ip not in self.jumps:
                    raise BrainfuckError(
                        'Unmatched bracket at pos %i' % (d_ip), 4)
            elif instr == ']':
                # Scan for matching bracket backwards
                heap = 0
                for ip in range(d_ip-1, -1, -1):
                    if code[ip] == ']':
                        heap += 1
                    elif code[ip] == '[':
                        if heap == 0:
                            self.jumps[d_ip] = ip
                            break
                        else:
                            heap -= 1
                if d_ip not in self.jumps:
                    raise BrainfuckError(
                        'Unmatched bracket at pos %i' % (d_ip), 4)
            d_ip += 1

        self.code = code

    def run(self, mem_size=30000, max_instr=-1):
        """
        Run the brainfuck code with a maximum number of instructions of
        max_instr (to counter infinite loops). If self.output is None, it
        returns the output instead of directly writing to the file descriptor.
        If debug is set to True, the interpreter will output debugging
        information during execution.
        """
        # Copy self references for speed.
        code = self.code
        input = self.input
        output = self.output
        jumps = self.jumps
        c_len = self.c_len

        icnt = 0             # Instruction counter against infinite loops
        mem = np.zeros([mem_size], dtype=np.uint8)  # Memory
        buf_out = b''         # Output buffer for tiny speed increase
        # Instruction pointer (current excecute place in code)
        ip = 0
        dp = 0               # Data pointer (current read/write place in mem)
        # Maximum Data Pointer (largest memory index access by code)

        while ip < c_len:
            if icnt > max_instr and max_instr >= 0:
                raise BrainfuckError('Maximum nr of instructions exceeded', 2)

            instr = code[ip]

            if instr == '+':
                mem[dp] += 1
            elif instr == '-':
                mem[dp] -= 1
            elif instr == '>':
                dp += 1
            elif instr == '<':
                dp -= 1
            elif instr == '[':
                if mem[dp] == 0:
                    ip = jumps[ip]
            elif instr == ']':
                if mem[dp] != 0:
                    ip = jumps[ip]
            elif instr == '.':
                buf_out += mem.item(dp).to_bytes(1, 'little')
            elif instr == ',':
                try:
                    mem[dp] = ord(input.read(1))
                except Exception:
                    mem[dp] = -1

            ip += 1
            icnt += 1

        output.write(str(buf_out, encoding='UTF-8'))
        if self.return_output:
            output.seek(0)
            return(output.read())


class TripleHorseDeer(Brainfuck):
    rep_operators = ['いぬい', 'とこ', 'アン', 'カト', 'さん', 'ばか', 'リゼ', 'エスタ']

    def __init__(self, code, input=sys.stdin, output=None):
        code = self._r2b(code).read()
        super().__init__(code, input, output)

    def _r2b(self, code):
        if isinstance(code, str):
            code = StringIO(code)
        out = StringIO()
        tc = 0
        while True:
            t = code.read(1)
            if t == '':
                break
            to = [i for i in self.rep_operators if i[tc] == t]
            if len(to) == 0:
                tc = 0
                continue
            if len(to) == 1:
                out.write(self.operators[(self.rep_operators.index(to[0]))])
                code.seek(code.tell() + len(to[0])-tc-1)
                tc = 0
                continue
            if len([i for i in to if len(i) == tc+1]) != 0:
                raise Exception('"rep_operators"の要素が競合しています')
            tc += 1
        out.seek(0)
        return out

    @classmethod
    def _b2r(cls, code):
        if isinstance(code, str):
            code = StringIO(code)
        out = StringIO()
        while True:
            t = code.read(1)
            if t == '':
                break
            if t in cls.operators:
                out.write(cls.rep_operators[cls.operators.index(t)])
        out.seek(0)
        return out
