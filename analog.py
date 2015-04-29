# MIPS Analog Machine
# Li Ao
# hi@leeleo.me

from utilities import RegisterList

CONST_MAXINTEGER = 2 ** 31 - 1
CONST_MAXUNSIGNEDINTEGER = 2 ** 32 - 1


class AssemblyAnalogMachine:
    def __init__(self):
        self._register = RegisterList()
        self.memory = [0] * 64 * 1024
        self._pc = 0
        self._npc = self._pc + 4
        self._HI = 0
        self._LO = 0

    def _add(self, rd, rs, rt):
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

    def _addu(self, rd, rs, rt):
        self._register[rd] = self._register[rs] + self._register[rt]
        self._advance_pc(4)

    def _and(self, rd, rs, rt):
        self._register[rd] = self._register[rs] & self._register[rt]
        self._advance_pc(4)

    def _break(self, rd, rs, rt):
        pass

    def _div(self, rs, rt):
        s_rs = self._get_signed_number(self._register[rs])
        s_rt = self._get_signed_number(self._register[rt])
        self._HI = int(s_rs / s_rt) & 0xffffffff
        self._LO = (s_rs % s_rt) & 0xffffffff
        self._advance_pc(4)

    def _divu(self, rs, rt):
        self._HI = int(self._register[rs] / self._register[rt]) & 0xffffffff
        self._LO = self._register[rs] % self._register[rt]
        self._advance_pc(4)

    def _mult(self, rs, rt):
        self._LO = self._register[rs] * self._register[rt] & 0xffffffff
        self._advance_pc(4)

    def _beq(self, rs, rt, offset):
        if self._register[rs] == self._register[rt]:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _bne(self, rs, rt, offset):
        if self._register[rs] != self._register[rt]:
            self._advance_pc(offset << 2)
        else:
            self._advance_pc(4)

    def _mfhi(self, rd):
        self._register[rd] = self._HI
        self._advance_pc(4)

    def _mflo(self, rd):
        self._register[rd] = self._LO
        self._advance_pc(4)

    def _get_signed_number(self, number):
        if number > CONST_MAXINTEGER:
            number -= CONST_MAXUNSIGNEDINTEGER + 1

    def _execute_instruction(self, instruction):
        pass

    def _advance_pc(self, offset):
        self._pc = self._npc
        self._npc += offset

    def import_file(self, path):
        file_type = path.split(',')[-1]
        if (file_type == 's'):
            pass
        elif (file_type == 'bin'):
            pass
        else:
            print("Error, invalid file type")

    def _overflow_handler(self):
        pass
