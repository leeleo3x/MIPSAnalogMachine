# MIPS Analog Machine
# Li Ao
# hi@leeleo.me

from utilities import RegisterList
from constants import *
import struct

CONST_MAXINTEGER = 2 ** 31 - 1
CONST_MAXUNSIGNEDINTEGER = 2 ** 32 - 1


class AssemblyAnalogMachine(object):
    execute_dict = {}

    def __init__(self):
        self._register = RegisterList()
        self.memory = [0] * 64 * 1024
        self.pc = 0
        self.npc = 4
        self._HI = 0
        self._LO = 0
        self._heap_pointer = 0
        self._stack_pointer = 0
        self.file_name = ""

    def _add(self, rd, rs, rt, shamt):
        res = self._register[rs] + self._register[rt]
        self._register[rd] = res

        if (
                self._register[rs] <= CONST_MAXINTEGER and
                self._register[rt] <= CONST_MAXINTEGER and
                res > CONST_MAXINTEGER
                or
                self._register[rs] > CONST_MAXINTEGER and
                self._register[rt] > CONST_MAXINTEGER and
                res <= CONST_MAXINTEGER
        ):
            self._overflow_handler()
        else:
            self._advance_pc(4)

    def _addi(self, rt, rs, immediate):
        res = self._register[rs] + immediate
        self._register[rt] = res
        self._advance_pc(4)

    def _addu(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rs] + self._register[rt]
        self._advance_pc(4)

    def _and(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rs] & self._register[rt]
        self._advance_pc(4)

    def _beq(self, rs, rt, offset):
        if self._register[rs] == self._register[rt]:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _bgez(self, rs, rt, offset):
        if self._register[rs] >= 0:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _bgezal(self, rs, rt, offset):
        if self._register[rs] >= 0:
            self._register[31] = self.pc + 8
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _bgtz(self, rs, rt, offset):
        if self._register[rs] > 0:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _blez(self, rs, rt, offset):
        if self._register[rs] <= 0:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _bltz(self, rs, rt, offset):
        if self._register[rs] < 0:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _bltzal(self, rs, rt, offset):
        if self._register[rs] < 0:
            self._register[31] = self.pc + 8
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _bne(self, rs, rt, offset):
        if self._register[rs] != self._register[rt]:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _break(self, rd, rs, rt, shamt):
        pass

    def _div(self, rd, rs, rt, shamt):
        s_rs = self._get_signed_number(self._register[rs])
        s_rt = self._get_signed_number(self._register[rt])
        self._HI = int(s_rs / s_rt) & 0xffffffff
        self._LO = (s_rs % s_rt) & 0xffffffff
        self._advance_pc(4)

    def _divu(self, rd, rs, rt, shamt):
        self._HI = int(self._register[rs] / self._register[rt]) & 0xffffffff
        self._LO = self._register[rs] % self._register[rt]
        self._advance_pc(4)

    def _j(self, target):
        self.pc = self.npc
        self.npc = (self.pc & 0xf0000000) | (target << 2)

    def _jal(self, target):
        self._register[31] = self.pc + 8
        self.pc = self.npc
        self.npc = (self.pc & 0xf0000000) | (target << 2)

    def _jr(self, rd, rs, rt, shamt):
        self.pc = self.npc
        self.npc = self._register[rs]

    def _lb(self, rt, rs, offset):
        self._register[rt] = self.memory[self._register[rs] + offset]
        self._advance_pc(4)

    def _lui(self, rt, rs, immediate):
        self._register[rt] = immediate << 16
        self._advance_pc(4)

    def _lw(self, rt, rs, offset):
        pos = self._register[rs] + offset
        word = self.memory[pos]
        word += self.memory[pos + 1] << 8
        word += self.memory[pos + 2] << 16
        word += self.memory[pos + 3] << 24
        self._register[rt] = word
        self._advance_pc(4)

    def _mfhi(self, rd, rs, rt, shamt):
        self._register[rd] = self._HI
        self._advance_pc(4)

    def _mflo(self, rd, rs, rt, shamt):
        self._register[rd] = self._LO
        self._advance_pc(4)

    def _mult(self, rd, rs, rt, shamt):
        self._LO = self._register[rs] * self._register[rt] & 0xffffffff
        self._advance_pc(4)

    def _noop(self, *argv):
        self._advance_pc(4)
        pass

    def _or(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rs] | self._register[rt]
        self._advance_pc(4)

    def _ori(self, rt, rs, immediate):
        self._register[rt] = self._register[rs] | immediate
        self._advance_pc(4)

    def _sb(self, rt, rs, offset):
        pos = self._register[rs] + offset
        self.memory[pos] = self._register[rt] & 0xff
        self._advance_pc(4)

    def _sll(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rt] << shamt
        self._advance_pc(4)

    def _sllv(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rs] << self._register[rt]
        self._advance_pc(4)

    def _slt(self, rd, rs, rt, shamt):
        s = self._get_signed_number(self._register[rs])
        t = self._get_signed_number(self._register[rt])
        if s < t:
            self._register[rd] = 1
        else:
            self._register[rd] = 0
        self._advance_pc(4)

    def _sra(self, rd, rs, rt, shamt):
        self._register[rd] = self._get_signed_number(self._register[rt]) >> shamt
        self._advance_pc(4)

    def _srl(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rt] >> shamt
        self._advance_pc(4)

    def _srlv(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rt] >> self._register[rs]
        self._advance_pc(4)

    def _sub(self, rd, rs, rt, shamt):
        s = self._get_signed_number(self._register[rs])
        t = self._get_signed_number(self._register[rt])
        self._register[rd] = s - t
        self._advance_pc(4)

    def _subu(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rs] - self._register[rt]
        self._advance_pc(4)

    def _sw(self, rt, rs, offset):
        pos = self._register[rs] + offset
        word = self._register[rt]
        self.memory[pos] = word & 0xff
        self.memory[pos + 1] = (word & 0xff00) >> 8
        self.memory[pos + 2] = (word & 0xff0000) >> 16
        self.memory[pos + 3] = (word & 0xff000000) >> 24
        self._advance_pc(4)

    def _syscall(self, rd, rs, rt, shamt):
        pass

    def _xor(self, rd, rs, rt, shamt):
        self._register[rd] = self._register[rs] ^ self._register[rt]
        self._advance_pc(4)

    def _empty(self, *para):
        self._advance_pc(4)
        pass

    def _get_signed_number(self, number):
        if number > CONST_MAXINTEGER:
            number -= CONST_MAXUNSIGNEDINTEGER + 1

    def _execute_r_type_instruction(self, instruction):
        function = instruction & 0x0000003f
        instruction_name = R_INSTRUCTIONS[function]
        if instruction_name == 'bad_function_code':
            func = self._empty
        else:
            instruction_name = '_' + instruction_name
            try:
                func = getattr(self, instruction_name)
            except AttributeError:
                func = self._empty
        rs = (instruction & 0x03e00000) >> 21
        rt = (instruction & 0x001f0000) >> 16
        rd = (instruction & 0x0000f800) >> 11
        shamt = (instruction & 0x000007c0) >> 6
        func(rd, rs, rt, shamt)

    def _execute_i_type_instruction(self, instruction):
        operation = (instruction & 0xfc000000) >> 26
        instruction_name = I_INSTRUCTIONS[operation]
        if instruction_name == 'bad_function_code':
            func = self._empty
        else:
            instruction_name = '_' + instruction_name
            try:
                func = getattr(self, instruction_name)
            except AttributeError:
                func = self._empty
        rs = (instruction & 0x03e00000) >> 21
        rt = (instruction & 0x001f0000) >> 16
        immediate = (instruction & 0x0000ffff)
        func(rt, rs, immediate)

    def _execute_j_type_instruction(self, instruction):
        operation = instruction & 0xfc000000
        target = instruction & 0x03ffffff
        instruction_name = J_INSTRUCTIONS[operation]
        if instruction_name == 'bad_function_code':
            func = self._empty
        else:
            instruction_name = '_' + instruction_name
            try:
                func = getattr(self, instruction_name)
            except AttributeError:
                func = self._empty
        func(target)

    def _execute_instruction(self, instruction):
        print("executing instruction: " + "{0:032b}".format(instruction))
        opcode = (instruction & 0xfc000000) >> 26
        if opcode == 0:
            self._execute_r_type_instruction(instruction)
        elif opcode == 2 or opcode == 3:
            self._execute_j_type_instruction(instruction)
        else:
            self._execute_i_type_instruction(instruction)

    def _advance_pc(self, offset):
        self.pc = self.npc
        self.npc += offset

    def import_data(self, path):
        with open(path, 'rb') as f:
            byte = f.read(1)
            while byte:
                self.memory[self._heap_pointer] = struct.unpack('B', byte)[0]
                self._heap_pointer += 1
                byte = f.read(1)
        print("Import data finished")

    def _execute_current_instruction(self):
        instruction = self.memory[self.pc]
        instruction += self.memory[self.pc + 1] << 8
        instruction += self.memory[self.pc + 2] << 16
        instruction += self.memory[self.pc + 3] << 24
        self._execute_instruction(instruction)

    def _print_register_data(self, *pos):
        if len(pos) == 0:
            for i in range(32):
                print("register[" + str(i) + "]: " + str(self._register[i]))
        else:
            try:
                re = int(pos[0])
                if re < 32:
                    print("register[" + str(re) + "]: " + str(self._register[re]))
                else:
                    print("Register address out of range!")
            except ValueError:
                print("Bad Instruction!")

    def _print_memory_data(self, pos):
        try:
            pos = int(pos)
            if pos < 64 * 1024:
                print("memory[" + str(pos) + "]: " + str(self._register[pos]))
            else:
                print("Memory address out of range!")
        except ValueError:
            print("Bad Instruction!")

    def _print_pointer_position(self):
        print("pc: " + str(self.pc))

    def run(self):
        while True:
            ins = input("(Analog): ").strip().lower().split()
            if ins[0] == "p":
                if len(ins) == 1:
                    self._print_register_data()
                else:
                    self._print_register_data(ins[1])
            elif ins[0] == "n":
                self._execute_current_instruction()
            elif ins[0] == "m":
                self._print_memory_data(ins[1])
            elif ins[0] == 'load':
                self.file_name = ins[1]
                try:
                    self.import_data(self.file_name)
                except:
                    print("Error while importing " + self.file_name)
            elif ins[0] == 's':
                self._print_pointer_position()

    def _overflow_handler(self):
        print("Warning: an overflow occurs")


def main():
    a = AssemblyAnalogMachine()
    a.run()

if __name__ == '__main__':
    main()
