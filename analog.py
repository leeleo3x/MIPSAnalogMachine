# MIPS Analog Machine
# Li Ao
# hi@leeleo.me

from utilities import RegisterList
from constants import *

CONST_MAXINTEGER = 2 ** 31 - 1
CONST_MAXUNSIGNEDINTEGER = 2 ** 32 - 1


class AssemblyAnalogMachine(object):
    execute_dict = {}

    def __init__(self):
        self.register = RegisterList()
        self.memory = [0] * 64 * 1024
        self.pc = 0
        self.HI = 0
        self.LO = 0
        self.heap_pointer = 0
        self.stack_pointer = 0

    def _add(self, rd, rs, rt):
        res = self.register[rs] + self.register[rt]
        self.register[rd] = res

        if (
                self.register[rs] <= CONST_MAXINTEGER and
                self.register[rt] <= CONST_MAXINTEGER and
                res > CONST_MAXINTEGER
                or
                self.register[rs] > CONST_MAXINTEGER and
                self.register[rt] > CONST_MAXINTEGER and
                res <= CONST_MAXINTEGER
        ):
            self._overflow_handler()
        else:
            self._advance_pc(4)

    def _addi(self, rt, rs, immediate):
        res = self.register[rs] + immediate
        self.register[rt] = res

    def _addu(self, rd, rs, rt):
        self.register[rd] = self.register[rs] + self.register[rt]
        self._advance_pc(4)

    def _and(self, rd, rs, rt):
        self.register[rd] = self.register[rs] & self.register[rt]
        self._advance_pc(4)

    def _slt(self, rd, rs, rt):
        s = self._get_signed_number(self.register[rs])
        t = self.register[rt]
        if s < t:
            self.register[rd] = 1
        else:
            self.register[rd] = 0
        self._advance_pc(4)

    def _break(self, rd, rs, rt):
        pass

    def _div(self, rd, rs, rt):
        s_rs = self._get_signed_number(self.register[rs])
        s_rt = self._get_signed_number(self.register[rt])
        self.HI = int(s_rs / s_rt) & 0xffffffff
        self.LO = (s_rs % s_rt) & 0xffffffff
        self._advance_pc(4)

    def _divu(self, rd, rs, rt):
        self.HI = int(self.register[rs] / self.register[rt]) & 0xffffffff
        self.LO = self.register[rs] % self.register[rt]
        self._advance_pc(4)

    def _mult(self, rd, rs, rt):
        self.LO = self.register[rs] * self.register[rt] & 0xffffffff
        self._advance_pc(4)

    def _beq(self, rs, rt, offset):
        if self.register[rs] == self.register[rt]:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _empty(self, **para):
        pass

    def _bne(self, rs, rt, offset):
        if self.register[rs] != self.register[rt]:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _mfhi(self, rd):
        self.register[rd] = self.HI
        self._advance_pc(4)

    def _mflo(self, rd):
        self.register[rd] = self.LO
        self._advance_pc(4)

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
        rs = (code & 0x03e00000) >> 21
        rt = (code & 0x001f0000) >> 16
        rd = (code & 0x0000f800) >> 11
        func(rd, rs, rt)

    def _execute_i_type_instruction(self, instruction):
        operation = instruction & 0xfc000000
        instruction_name = I_INSTRUCTIONS[operation]
        if instruction_name == 'bad_function_code':
            func = self._empty
        else:
            instruction_name = '_' + instruction_name
            try:
                func = getattr(self, instruction_name)
            except AttributeError:
                func = self._empty
        rs = (code & 0x03e00000) >> 21
        rt = (code & 0x001f0000) >> 16
        immediate = (code & 0x0000ffff)
        func(rs, rt, immediate)

    def _execeute_j_type_instruction(self, instruction):
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
        pass

    def _advance_pc(self, offset):
        self.pc += offset

    def import_data(self, path):
        with open(path, 'rb') as f:
            byte = f.read(1)
            while byte:
                self.memory[self._heap_pointer + 1] = byte
                self._heap_pointer += 1
                byte = f.read(1)

    def _overflow_handler(self):
        pass


def main():
    a = AssemblyAnalogMachine()
    print(a.execute_dict)
    for i in range(2 ** 6):
        a._execute_r_instruction(i)

if __name__ == '__main__':
    main()
