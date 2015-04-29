# MIPS Analog Machine Utilities
# Li Ao
# hi@leeleo.me


class RegisterList(list):
    def __setitem__(self, key, value):
        if key == 0:
            return
        if key > 31:
            return
        value = value & 0xffffffff
        super().__setitem__(key, value)

    def __init__(self):
        super().__init__([0] * 32)

    def append(self, value):
        print("You are not supposed to modify the register list size")

    def pop(self):
        print("You are not supposed to modify the register list size")
