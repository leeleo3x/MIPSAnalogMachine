REGISTER = {
    '$zero': 0,
    '$at': 1,
    '$v0': 2,
    '$v1': 3,
    '$a0': 4,
    '$a1': 5,
    '$a2': 6,
    '$a3': 7,
    '$t0': 8,
    '$t1': 9,
    '$t2': 10,
    '$t3': 11,
    '$t4': 12,
    '$t5': 13,
    '$t6': 14,
    '$t7': 15,
    '$s0': 16,
    '$s1': 17,
    '$s2': 18,
    '$s3': 19,
    '$s4': 20,
    '$s5': 21,
    '$s6': 22,
    '$s7': 23,
    '$t8': 24,
    '$t9': 25,
    '$k0': 26,
    '$k1': 27,
    '$gp': 28,
    '$sp': 29,
    '$fp': 30,
    '$ra': 31
}

REGISTER_INV = [
    '$zero',
    '$at',
    '$v0',
    '$v1',
    '$a0',
    '$a1',
    '$a2',
    '$a3',
    '$t0',
    '$t1',
    '$t2',
    '$t3',
    '$t4',
    '$t5',
    '$t6',
    '$t7',
    '$s0',
    '$s1',
    '$s2',
    '$s3',
    '$s4',
    '$s5',
    '$s6',
    '$s7',
    '$t8',
    '$t9',
    '$k0',
    '$k1',
    '$gp',
    '$sp',
    '$fp',
    '$ra'
]

OPERATION = {
    'add': [32, 0],
    'sub': [34, 0],
    'slt': [42, 0],
    'lw': [35, 2],
    'sw': [43, 2],
    'beq': [4, 3],
    'bne': [5, 3],
    'addi': [8, 4],
    'j': [2, 1],
    'jal': [3, 1],
    'noop': [0, 0]
}

R_INSTRUCTIONS = [
    'sll',
    'bad_function_code',
    'srl',
    'sra',
    'sllv',
    'bad_function_code',
    'srlv',
    'srav',
    'jr',
    'jalr',
    'bad_function_code',
    'bad_function_code',
    'syscall',
    'break',
    'bad_function_code',
    'bad_function_code',
    'mfhi',
    'mthi',
    'mflo',
    'mtlo',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'mult',
    'multu',
    'div',
    'divu',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'add',
    'addu',
    'sub',
    'subu',
    'and',
    'or',
    'xor',
    'nor',
    'bad_function_code',
    'bad_function_code',
    'slt',
    'sltu',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code'
]

J_INSTRUCTIONS = [
    'bad_function_code',
    'bad_function_code',
    'j',
    'jal'
]

I_INSTRUCTIONS = [
    'bad_function_code',
    'bltz',
    'bad_function_code',
    'bad_function_code',
    'beq',
    'bne',
    'blez',
    'bgtz',
    'addi',
    'addiu',
    'slti',
    'sltiu',
    'andi',
    'ori',
    'xori',
    'lui',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'lb',
    'lh',
    'bad_function_code',
    'lw',
    'lbu',
    'lhu',
    'bad_function_code',
    'bad_function_code',
    'sb',
    'sh',
    'bad_function_code',
    'sw',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'lwc1',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'swc1',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code',
    'bad_function_code'
]
