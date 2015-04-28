#
# MIPS Assembly Decoder
#

import sys
import struct
from constants import REGISTER_INV, R_INSTRUCTIONS, J_INSTRUCTIONS, I_INSTRUCTIONS, OPERATION

class AssemblyDecoder:
    def __init__(self):
        self._assembly_code = []
        self._assembly_instruction = []
        self._opath = ""

    def process_file(self, path, opath = ""):
        if not opath:
            opath = path + '.s'
        self._opath = opath
        self._import_data(path)
        self._analyze_assembly_code()
        self._write_to_file()

    def _import_data(self, path):
        with open(path, 'rb') as f:
            byte4 = f.read(4)
            while byte4:
                print(byte4)
                self._assembly_code.append(struct.unpack('I', byte4)[0])
                byte4 = f.read(4)
        print(self._assembly_code)

    def _analyze_assembly_code(self):
        for code in self._assembly_code:
            print('{0:032b}'.format(code))
            instruction = []
            operation = (code & 0xfc000000) >> 26
            print(operation)
            if operation == 0:
                function = code & 0x0000003f
                if [R_INSTRUCTIONS[function]] == 'bad_function_code':
                    print("Error while processing code:", code)
                    continue
                instruction.append(R_INSTRUCTIONS[function])
                rs = (code & 0x03e00000) >> 21
                rt = (code & 0x001f0000) >> 16
                rd = (code & 0x0000f800) >> 11
                shamt = (code & 0x000008c0) >> 6

                instruction.append(REGISTER_INV[rd])
                instruction.append(REGISTER_INV[rs])
                instruction.append(REGISTER_INV[rt])
            elif operation == 2 or operation == 3:
                instruction.append(J_INSTRUCTIONS[operation])
                immediate = code & 0x03ffffff
                immediate = immediate << 2
                instruction.append(immediate)
            else:
                rs = (code & 0x03e00000) >> 21
                rt = (code & 0x001f0000) >> 16
                immediate = code & 0x0000ffff
                if operation == 1:
                    if rt == 0:
                        instruction.append('bltz')
                    elif rt == 1:
                        instruction.append('bgez')
                    else:
                        print("Error while processing code:", code)
                        continue
                else:
                    if I_INSTRUCTIONS[operation] == "bad_function_code":
                        print("Error while processing code:", code)
                        continue
                    else:
                        instruction.append(I_INSTRUCTIONS[operation])
                if OPERATION[instruction[0]][1] == 1:
                    instruction.append(REGISTER_INV[rt])
                    s = "{}({})".format(immediate, REGISTER_INV[rs])
                    instruction.append(s)
                elif OPERATION[instruction[0]][1] == 3:
                    instruction.append(REGISTER_INV[rs])
                    instruction.append(REGISTER_INV[rt])
                    instruction.append(immediate)
                elif OPERATION[instruction[0]][1] == 4:
                    instruction.append(REGISTER_INV[rt])
                    instruction.append(REGISTER_INV[rs])
                    instruction.append(immediate)
            print(instruction)
            self._assembly_instruction.append(instruction)

    def _write_to_file(self):
        with open(self._opath, "w+") as f:
            for instruction in self._assembly_instruction:
                string = ""
                for ins in instruction:
                    string += str(ins) + " "
                string += "\n"
                f.write(string)



def main():
    argv = sys.argv
    if not ((len(argv) == 2) or (len(argv) == 3)):
        print("Usage: ./decode.py input [output]")
        return
    decoder = AssemblyDecoder()
    if len(argv) == 2:
        decoder.process_file(argv[1])
    else:
        decoder.process_file(argv[1], argv[2])

if __name__ == '__main__':
    main()

