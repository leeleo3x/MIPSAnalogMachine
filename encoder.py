import re
import sys
import struct
from constants import *


class AssemblyEncoder(object):

    def __init__(self):
        self._lines = []
        self._address = {}
        self._codes = []
        self._filename = ""
        self._opath = ""
        self._start_address = 0

    @property
    def start_address(self):
        return self._start_address

    @start_address.setter
    def start_address(self, address):
        self._start_address = address

    def process_file(self, path, opath=""):
        if not opath:
            opath = path + '.bin'
        self._import_data(path)
        self._pre_analyze()
        self._opath = opath
        for i in range(len(self._lines)):
            self._analyze_per_line(i)
        self._generate_binary_file()

    def _import_data(self, path):
        self._lines = [
            line.strip().replace(',', ' ').lower().split()
            for line in open(path)
        ]

    def _pre_analyze(self):
        for i in range(len(self._lines)):
            if self._lines[i][0] not in OPERATION.keys():
                self._address[self._lines[i][0].replace(':', '')] = i * 4 + self._start_address
                self._lines[i].pop(0)

    def _analyze_r_type_assembly_instruction(self, instruction):
        code = 0
        code &= 0x06ffffff
        register = instruction[1:4]
        if len(register) != 3:
            print("Invalid register sum")
            return 0
        for reg in register:
            if reg not in REGISTER:
                print("Invalid register identifier:", reg)
                return 0
        code |= REGISTER[register[0]] << 11
        code |= REGISTER[register[1]] << 21
        code |= REGISTER[register[2]] << 16
        code |= OPERATION[instruction[0]][0]
        return code

    def _analyse_j_type_assembly_instruction(self, instruction):
        code = 0
        operation = OPERATION[instruction[0]]
        code |= operation[0] << 26
        if instruction[1] in self._address:
            addr = self._address[instruction[1]] >> 2
            print(addr)
            code |= addr & 0x3ffffff
        else:
            try:
                addr = int(self._eval(instruction[1]))
                addr = addr >> 2
                code |= addr & 0x3ffffff
            except NameError:
                print("Invalid expression syntax")
                return 0
        return code

    def _analyze_i_type_assembly_instruction(self, instruction, pos):
        code = 0
        operation = OPERATION[instruction[0]]
        if operation[1] == 2:
            code |= operation[0] << 26
            if instruction[1] not in REGISTER:
                print("Invalid register identifier:", instruction[1])
                return 0
            search_string = r"([0-9\+\-\*/]+)\(([$][a-z][0-9]{1,2})\)"
            engine = re.compile(search_string)
            result = engine.findall(instruction[2])[0]
            if len(result) != 2 or result[1] not in REGISTER:
                print("Invalid format")
                return 0
            code |= REGISTER[instruction[1]] << 16
            code |= REGISTER[result[1]] << 21
            try:
                code |= int(self._eval(result[0])) & 0xffff
            except NameError:
                print("Invalid expression syntax")
                return 0
        elif operation[1] == 3:
            register = instruction[1:4]
            print(register)
            try:
                addr = int(register[2])
                addr = addr >> 2
                code |= addr & 0x1c
            except ValueError:
                if register[2] not in self._address:
                    return 0
                addr = self._address[register[2]]\
                    - pos * 4 - 4 - self._start_address
                addr = addr >> 2
                code |= addr & 0xffff
            register.pop(2)
            for reg in register:
                if reg not in REGISTER:
                    print("Invalid register identifier:", reg)
                    return 0
            code |= REGISTER[register[0]] << 21
            code |= REGISTER[register[1]] << 16
            code |= OPERATION[instruction[0]][0] << 26
        elif operation[1] == 4:
            register = instruction[1:3]
            for reg in register:
                if reg not in REGISTER_INV:
                    print("Invalid register identifier:", reg)
                    return 0
            code |= REGISTER[register[1]] << 21
            code |= REGISTER[register[0]] << 16
            try:
                immediate = int(instruction[3])
                immediate = immediate >> 2
                code |= immediate & 0x1c
            except ValueError:
                print("Invalid immediate")
                return 0
        return code


    def _analyze_per_line(self, pos):
        data = self._lines[pos]
        print("Processing the ", pos, "line")
        print(data)
        if data[0] not in OPERATION.keys():
            print("ERROR: failed while processing:", pos, "line")
            print("Invalid operation identifier:", data[0])
            self._codes.append(0)
            return
        operation = OPERATION[data[0]]
        if operation[1] == 0:
            code = self._analyze_r_type_assembly_instruction(data)
        elif operation[1] == 1:
            code = self._analyse_j_type_assembly_instruction(data)
        else:
            code = self._analyze_i_type_assembly_instruction(data, pos)
        print(code)
        self._codes.append(code)

    def _generate_binary_file(self):
        with open(self._opath, 'bw+') as f:
            for code in self._codes:
                f.write(struct.pack('I', code))
        f.close

    def _eval(self, expression):
        ns = {'__builtins__': None}
        num = eval(expression, ns)
        return num

def main():
    argv = sys.argv
    if not ((len(argv) == 2) or (len(argv) == 3)):
        print("Usage: ./encoder.py input [output]")
        return
    encoder = AssemblyEncoder()
    if len(argv) == 2:
        encoder.process_file(argv[1])
    else:
        encoder.process_file(argv[1], argv[2])

if __name__ == "__main__":
    main()
