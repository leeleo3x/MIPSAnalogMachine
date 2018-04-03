# Assembler & Disassembler Simulator

[Chinese Version](doc.md)

#### Ao Li, 3130001009 hi@leeleo.me

## Assembler

### How to run

    python3 encoder.py input [output]

### Algorithm Intros

- Read the asm by line
- Remove unecessary characters
- Store each instruction by syntax token
- Use RegExp to extract necessary information
- Match preserved keywords with extracted infomation and translate them into assembly codes
- Translate the asm code into binary file

## Disassembler

### How to run

    python3 decoder.py input [output]

### Algorithm Intros

- Read the binary file
- Translate each 32 bits to a Int type
- Analyse 32 bits and translate to assembly codes
- Format the asm 
- Output the foramtted asm to file

## Simulator

- Simulate `debug` working mode
- Read the binary file into memory
- Simulate the assembly code

- Basic Instruction

    - `file file_name` - Read a binary file
    - `n` - Execute one instruction
    - `p [pos]` - Output the content of `pos` register; if no specific `pos` is given, then output the content of all registers
    - `m pos` - Output the content of `pos` pointing to
    - `s` - Output the address of current PC pointer

- This simulator considered the situation of `delay slot`, so we recommend to insert a `noop` instruction after all `delay slot` instructions.
