from binaryninja import *
import struct
import os

REGISTER = 0
IOREGISTER = 1
ADDRESS = 2
INDIR_ADDR = 3
IMMEDIATE = 4
T = 5
DES = 6
REL_ADDR = 7

OperandTokenGen = [
    lambda reg, addr, instr: [ # REGISTER
        InstructionTextToken(InstructionTextTokenType.RegisterToken, reg)
    ],
    lambda reg, addr, instr: [ # IOREGISTER
        InstructionTextToken(InstructionTextTokenType.RegisterToken, reg)
    ],
    lambda reg, addr, instr: [ # ADDRESS
            InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(reg*2), reg*2)
    ],
    lambda reg, addr, instr: [ # INDIR_ADDR
        InstructionTextToken(InstructionTextTokenType.TextToken, reg)
    ],
    lambda reg, addr, instr: [ # IMMEDIATE
        InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(reg), reg)
    ],
    lambda reg, addr, instr: [ # T
        InstructionTextToken(InstructionTextTokenType.TextToken, reg)
    ],
    lambda reg, addr, instr: [ # DES
        InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(reg), reg)
    ],
    lambda reg, addr, instr: [ #REL_ADDR
        InstructionTextToken(InstructionTextTokenType.PossibleAddressToken,hex(reg*2) + ', ' + hex(addr+reg*2+1*2).replace('L',''), addr+reg*2+1*2)
    ]
]

Registers = [
    'r0',
    'r1',
    'r2',
    'r3',
    'r4',
    'r5',
    'r6',
    'r7',
    'r8',
    'r9',
    'r10',
    'r11',
    'r12',
    'r13',
    'r14',
    'r15',
    'r16',
    'r17',
    'r18',
    'r19',
    'r20',
    'r21',
    'r22',
    'r23',
    'r24',
    'r25',
    'r26',
    'r27',
    'r28',
    'r29',
    'r30',
    'r31'
]

IORegisters = [
    'Reserved',
    'Reserved',
    'Reserved',
    'PINB',
    'DDRB',
    'PORTB',
    'PINC',
    'DDRC',
    'PORTC',
    'PIND',
    'DDRD',
    'PORTD',
    'Reserved',
    'Reserved',
    'Reserved',
    'Reserved',
    'Reserved',
    'Reserved',
    'Reserved',
    'Reserved',
    'Reserved',
    'TIFR0',
    'TIFR1',
    'TIFR2',
    'Reserved',
    'Reserved',
    'Reserved',
    'PCIFR',
    'EIFR',
    'EIMSK',
    'GPIOR0',
    'EECR',
    'EEDR',
    'EEARL',
    'EEARH',
    'GTCCR',
    'TCCR0A',
    'TCCR0B',
    'TCNT0',
    'OCR0A',
    'OCR0B',
    'Reserved',
    'GPIOR1',
    'GPIOR2',
    'SPCR',
    'SPSR',
    'SPDR',
    'Reserved',
    'ACSR',
    'Reserved',
    'Reserved',
    'SMCR',
    'MCUSR',
    'MCUCR',
    'Reserved',
    'SPMCSR',
    'Reserved',
    'Reserved',
    'Reserved',
    'Reserved',
    'Reserved',
    'SPL',
    'SPH',
    'SREG'
]

def GetOperands(instr, instruction):
    src, src_operand_type, dst, dst_operand_type = None, None, None, None

    if instr == 'movw':
        src = Registers[instruction&0x000f]
        dst = Registers[(instruction&0x00f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'muls':
        src = Registers[16 + (instruction&0x000f)]
        dst = Registers[16 + ((instruction&0x00f0)>>4)]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'mulsu':
        src = Registers[16 + (instruction&0x0007)]
        dst = Registers[16 + ((instruction&0x0070)>>4)]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'fmul':
        src = Registers[16 + (instruction&0x0007)]
        dst = Registers[16 + ((instruction&0x0070)>>4)]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'fmuls':
        src = Registers[16 + (instruction&0x0007)]
        dst = Registers[16 + ((instruction&0x0070)>>4)]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'fmulsu':
        src = Registers[16 + (instruction&0x0007)]
        dst = Registers[16 + ((instruction&0x0070)>>4)]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'cpc':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'sub':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'sbc':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'cp':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'add':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'adc':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'rol':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'lsl':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'cpse':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'and':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'eor':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'or':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'mov':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'cpi':
        src = (((instruction&0x0f00)>>4) + (instruction&0x000f))
        dst = Registers[16 + ((instruction&0x00f0)>>4)]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    elif instr == 'sbci':
        src = (((instruction&0x0f00)>>4) + (instruction&0x000f))
        dst = Registers[16 + ((instruction&0x00f0)>>4)]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    elif instr == 'subi':
        src = (((instruction&0x0f00)>>4) + (instruction&0x000f))
        dst = Registers[16 + ((instruction&0x00f0)>>4)]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    # elif instr == 'sbi':
    #     src = (instruction&0x0f00)>>4 + (instruction&0x000f)
    #     dst = Registers[16 + instruction&0x00f0>>4]
    elif instr == 'ori':
        src = (((instruction&0x0f00)>>4) + (instruction&0x000f))
        dst = Registers[16 + ((instruction&0x00f0)>>4)]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    # elif instr == 'cbr':
    #     src = (instruction&0x0f00)>>4 + (instruction&0x000f)
    #     dst = Registers[16 + instruction&0x00f0>>4]
    elif instr == 'andi':
        src = (((instruction&0x0f00)>>4) + (instruction&0x000f))
        dst = Registers[16 + ((instruction&0x00f0)>>4)]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    elif instr == 'ldd':
        if (((instruction&0x0008)>>3) == 0):
            src = 'z+' + str(instruction&0x0007 + ((instruction&0x0c00)>>7) + ((instruction&0x2000)>>8))
        else:
            src = 'y+' + str(instruction&0x0007 + ((instruction&0x0c00)>>7) + ((instruction&0x2000)>>8))
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = INDIR_ADDR
        dst_operand_type = REGISTER
    elif instr == 'std':
        if ((instruction&0x0008)>>3 == 0):
            dst = 'z+' + str(instruction&0x0007 + ((instruction&0x0c00)>>7) + ((instruction&0x2000)>>8))
        else:
            dst = 'y+' + str(instruction&0x0007 + ((instruction&0x0c00)>>7) + ((instruction&0x2000)>>8))
        src = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = INDIR_ADDR
    elif instr == 'lds':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = ADDRESS
        dst_operand_type = REGISTER
    elif instr == 'sts':
        src = Registers[(instruction&0x01f0)>>4]
        dst = None
        src_operand_type = REGISTER
        dst_operand_type = ADDRESS
    elif instr == 'ld':
        if ((instruction&0x000f) == 0):
            src = 'z'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 1):
            src = 'z+'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 8):
            src = 'y'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 9):
            src = 'y+'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 2):
            src = '-z'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 0xa):
            src = '-y'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 0xc):
            src = 'x'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 0xd):
            src = 'x+'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 0xe):
            src = '-x'
            dst = Registers[(instruction&0x01f0)>>4]
        else:
            src = None
            dst = None
        src_operand_type = INDIR_ADDR
        dst_operand_type = REGISTER
    elif instr == 'st':
        if ((instruction&0x000f) == 0):
            src = Registers[(instruction&0x01f0)>>4]
            dst = 'z'
        elif ((instruction&0x000f) == 1):
            src = Registers[(instruction&0x01f0)>>4]
            dst = 'z+'
        elif ((instruction&0x000f) == 8):
            src = Registers[(instruction&0x01f0)>>4]
            dst = 'y'
        elif ((instruction&0x000f) == 9):
            src = Registers[(instruction&0x01f0)>>4]
            dst = 'y+'
        elif ((instruction&0x000f) == 2):
            src = Registers[(instruction&0x01f0)>>4]
            dst = '-z'
        elif ((instruction&0x000f) == 0xa):
            src = Registers[(instruction&0x01f0)>>4]
            dst = '-y'
        elif ((instruction&0x000f) == 0xc):
            src = Registers[(instruction&0x01f0)>>4]
            dst = 'x'
        elif ((instruction&0x000f) == 0xd):
            src = Registers[(instruction&0x01f0)>>4]
            dst = 'x+'
        elif ((instruction&0x000f) == 0xe):
            src = Registers[(instruction&0x01f0)>>4]
            dst = '-x'
        else:
            src = None
            dst = None
        src_operand_type = REGISTER
        dst_operand_type = INDIR_ADDR
    elif instr == 'lpm':
        if ((instruction&0x000f) == 4):
            src = 'z'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 5):
            src = 'z+'
            dst = Registers[(instruction&0x01f0)>>4]
        else:
            src = None
            dst = None
        src_operand_type = INDIR_ADDR
        dst_operand_type = REGISTER
    elif instr == 'elpm':
        if ((instruction&0x000f) == 6):
            src = 'z'
            dst = Registers[(instruction&0x01f0)>>4]
        elif ((instruction&0x000f) == 7):
            src = 'z+'
            dst = Registers[(instruction&0x01f0)>>4]
        else:
            src = None
            dst = None
        src_operand_type = INDIR_ADDR
        dst_operand_type = REGISTER
    elif instr == 'xch':
        src = Registers[(instruction&0x01f0)>>4]
        dst = 'z'
        src_operand_type = REGISTER
        dst_operand_type = INDIR_ADDR
    elif instr == 'las':
        src = Registers[(instruction&0x01f0)>>4]
        dst = 'z'
        src_operand_type = REGISTER
        dst_operand_type = INDIR_ADDR
    elif instr == 'lac':
        src = Registers[(instruction&0x01f0)>>4]
        dst = 'z'
        src_operand_type = REGISTER
        dst_operand_type = INDIR_ADDR
    elif instr == 'lat':
        src = Registers[(instruction&0x01f0)>>4]
        dst = 'z'
        src_operand_type = REGISTER
        dst_operand_type = INDIR_ADDR
    elif instr == 'push':
        src = Registers[(instruction&0x01f0)>>4]
        dst = None
        src_operand_type = REGISTER
        dst_operand_type = None
    elif instr == 'pop':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'com':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'neg':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'swap':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'inc':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'asr':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'lsr':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'ror':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'dec':
        src = None
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = None
        dst_operand_type = REGISTER
    elif instr == 'des':
        src = None
        dst = ((instruction&0x00f0)>>4)
        src_operand_type = None
        dst_operand_type = DES
    elif instr == 'jmp':
        src = None
        dst = None
        src_operand_type = None
        dst_operand_type = ADDRESS
    elif instr == 'call':
        src = None
        dst = None
        src_operand_type = None
        dst_operand_type = ADDRESS
    elif instr == 'adiw':
        src = (((instruction&0x00c0)>>2) + (instruction&0x000f))
        if ((instruction&0x0030)>>4 == 0):
            dst = 'r25:r24'
        elif ((instruction&0x0030)>>4 == 1):
            dst = 'x'
        elif ((instruction&0x0030)>>4 == 2):
            dst = 'y'
        elif ((instruction&0x0030)>>4 == 3):
            dst = 'z'
        else:
            dst = None
        src_operand_type = IMMEDIATE
        dst_operand_type = INDIR_ADDR
    elif instr == 'sbiw':
        src = (((instruction&0x00c0)>>2) + (instruction&0x000f))
        if ((instruction&0x0030)>>4 == 0):
            dst = 'r25:r24'
        elif ((instruction&0x0030)>>4 == 1):
            dst = 'x'
        elif ((instruction&0x0030)>>4 == 2):
            dst = 'y'
        elif ((instruction&0x0030)>>4 == 3):
            dst = 'z'
        else:
            dst = None
        src_operand_type = IMMEDIATE
        dst_operand_type = INDIR_ADDR
    elif instr == 'cbi':
        src = (instruction&0x0007)
        dst = IORegisters[(instruction&0x00f8)>>3]
        src_operand_type = IMMEDIATE
        dst_operand_type = IOREGISTER
    elif instr == 'sbi':
        src = (instruction&0x0007)
        dst = IORegisters[(instruction&0x00f8)>>3]
        src_operand_type = IMMEDIATE
        dst_operand_type = IOREGISTER
    elif instr == 'sbic':
        src = (instruction&0x0007)
        dst = IORegisters[(instruction&0x00f8)>>3]
        src_operand_type = IMMEDIATE
        dst_operand_type = IOREGISTER
    elif instr == 'sbis':
        src = (instruction&0x0007)
        dst = IORegisters[(instruction&0x00f8)>>3]
        src_operand_type = IMMEDIATE
        dst_operand_type = IOREGISTER
    elif instr == 'mul':
        src = Registers[((instruction&0x0200)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = REGISTER
        dst_operand_type = REGISTER
    elif instr == 'in':
        src = IORegisters[((instruction&0x0600)>>5) + (instruction&0x000f)]
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = IOREGISTER
        dst_operand_type = REGISTER
    elif instr == 'out':
        src = Registers[(instruction&0x01f0)>>4]
        dst = IORegisters[((instruction&0x0600)>>5) + (instruction&0x000f)]
        src_operand_type = REGISTER
        dst_operand_type = IOREGISTER
    elif instr == 'rjmp':
        src = None
        dst = (instruction&0x0fff)
        if ((dst&0x0800)>>11) == 0:
            dst = dst
        else:
            dst = dst - (1 << 12)
        src_operand_type = None
        dst_operand_type = REL_ADDR
    elif instr == 'rcall':
        src = None
        dst = (instruction&0x0fff)
        if ((dst&0x0800)>>11) == 0:
            dst = dst
        else:
            dst = dst - (1 << 12)
        src_operand_type = None
        dst_operand_type = REL_ADDR
    elif instr == 'ldi':
        src = (((instruction&0x0f00)>>4) + (instruction&0x000f))
        dst = Registers[16 + ((instruction&0x00f0)>>4)]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    elif instr == 'brbs':
        src = ((instruction&0x03f8)>>3)
        if ((src&0x40)>>6) == 0:
            src = src
        else:
            src = src - (1 << 7)
        dst = (instruction&0x0007)
        src_operand_type = REL_ADDR
        dst_operand_type = IMMEDIATE
    elif instr == 'brbc':
        src = ((instruction&0x03f8)>>3)
        if ((src&0x40)>>6) == 0:
            src = src
        else:
            src = src - (1 << 7)
        dst = (instruction&0x0007)
        src_operand_type = REL_ADDR
        dst_operand_type = IMMEDIATE
    elif (instr == 'breq' or instr == 'brne' or instr == 'brcs'
            or instr == 'brcc' or instr == 'brsh' or instr == 'brlo'
            or instr == 'brmi' or instr == 'brpl' or instr == 'brge'
            or instr == 'brlt' or instr == 'brhs' or instr == 'brhc'
            or instr == 'brts' or instr == 'brtc' or instr == 'brvs'
            or instr == 'brvc' or instr == 'brie' or instr == 'brid'):
        src = None
        dst = ((instruction&0x03f8)>>3)
        if ((dst&0x40)>>6) == 0:
            dst = dst
        else:
            dst = dst - (1 << 7)
        src_operand_type = None
        dst_operand_type = REL_ADDR
    elif instr == 'bld':
        src = (instruction&0x0007)
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    elif instr == 'bst':
        src = (instruction&0x0007)
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    elif instr == 'sbrc':
        src = (instruction&0x0007)
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER
    elif instr == 'sbrs':
        src = (instruction&0x0007)
        dst = Registers[(instruction&0x01f0)>>4]
        src_operand_type = IMMEDIATE
        dst_operand_type = REGISTER

    return src, src_operand_type, dst, dst_operand_type


def get_instr_name(instruction, high_msn):
    #https://en.wikipedia.org/wiki/Atmel_AVR_instruction_set
    if high_msn == 0x0:
        if ((instruction&0x0f00)>>8 == 0x1):
            return 'movw'
        elif ((instruction&0x0f00)>>8 == 0x2):
            return 'muls'
        elif ((instruction&0x0f00)>>8 == 0x3):
            if ((instruction&0x0080) == 0 and (instruction&0x0004) == 0):
                return 'mulsu'
            elif ((instruction&0x0080) == 0 and (instruction&0x0004) != 0):
                return 'fmul'
            elif ((instruction&0x0080) != 0 and (instruction&0x0004) == 0):
                return 'fmuls'
            elif ((instruction&0x0080) != 0 and (instruction&0x0004) != 0):
                return 'fmulsu'
            else:
                return None
        elif ((instruction&0x0400)>>8 == 0x4):
            return 'cpc'
        elif ((instruction&0x0800)>>8 == 0x8):
            return 'sbc'
        elif ((instruction&0x0c00)>>8 == 0xc):
            if(((instruction&0x00f0)>>4 == (instruction&0x000f)) and ((instruction&0x0200)>>1 == (instruction&0x0100))):
                return 'lsl'
            else:
                return 'add'
        else:
            return None

    elif high_msn == 0x1:
        if ((instruction&0x0c00)>>10 == 0x0):
            return 'cpse'
        elif ((instruction&0x0c00)>>10 == 0x1):
            return 'cp'
        elif ((instruction&0x0c00)>>10 == 0x2):
            return 'sub'
        elif ((instruction&0x0c00)>>10 == 0x3):
            if(((instruction&0x00f0)>>4 == (instruction&0x000f)) and ((instruction&0x0200)>>1 == (instruction&0x0100))):
                return 'rol'
            else:
                return 'adc'
        else:
            return None

    elif high_msn == 0x2:
        if ((instruction&0x0c00)>>10 == 0x0):
            return 'and'
        elif ((instruction&0x0c00)>>10 == 0x1):
            return 'eor'
        elif ((instruction&0x0c00)>>10 == 0x2):
            return 'or'
        elif ((instruction&0x0c00)>>10 == 0x3):
            return 'mov'
        else:
            return None

    elif high_msn == 0x3:
        return 'cpi'

    elif high_msn == 0x4:
        return 'sbci'

    elif high_msn == 0x5:
        return 'subi'

    elif high_msn == 0x6: #Technically is both ORI and SBR as they perform the same operation
        return 'ori'
        #return 'sbr'

    elif high_msn == 0x7: #Technically is both ANDI and CBR as they perform the same operation
        return 'andi'
        #return 'cbr'

    elif high_msn == 0x8: #TODO These should be ld and ldd as well as st and std (but ldd z+0 is the same as ld z)
        if ((instruction&0x0200) == 0):
            return 'ldd'
        elif ((instruction&0x0200) != 0):
            return 'std'
        else:
            return None

    elif high_msn == 0x9:
        if ((instruction&0x0c00)>>10 == 0):
            if ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 0):
                return 'lds'
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 0):
                return 'sts'
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 1):
                return 'ld' #Possibly a ld z+
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 1):
                return 'st' #Possibly a st z+
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 9):
                return 'ld' #Possibly a ld y+
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 9):
                return 'st' #Possibly a st y+
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 2):
                return 'ld' #Possibly a ld -z
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 2):
                return 'st' #Possibly a st -z
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 0xa):
                return 'ld' #Possibly a ld -y
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 0xa):
                return 'st' #Possibly a st -y
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 4):
                return 'lpm' #lpm Rd, Z
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 6):
                return 'elpm' #elpm Rd, Z
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 5):
                return 'lpm' #lpm Rd, Z+
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 7):
                return 'elpm' #elpm Rd, Z+
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 4):
                return 'xch'
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 5):
                return 'las'
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 6):
                return 'lac'
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 7):
                return 'lat'
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 0xc):
                return 'ld' #ld X
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 0xc):
                return 'st' #st X
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 0xd):
                return 'ld' #ld X+
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 0xd):
                return 'st' #st X+
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 0xe):
                return 'ld' #ld -X
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 0xe):
                return 'st' #st -X
            elif ((instruction&0x0200)>>9 == 0 and (instruction&0x000f) == 0xf):
                return 'pop' #pop rd
            elif ((instruction&0x0200)>>9 == 1 and (instruction&0x000f) == 0xf):
                return 'push' #push rd
            else:
                return None
        elif ((instruction&0x0c00)>>10 == 1):
            if ((instruction&0x0200)>>9 == 0):
                if ((instruction&0x000f) == 0):
                    return 'com'
                elif ((instruction&0x000f) == 1):
                    return 'neg'
                elif ((instruction&0x000f) == 2):
                    return 'swap'
                elif ((instruction&0x000f) == 3):
                    return 'inc'
                elif ((instruction&0x000f) == 5):
                    return 'asr'
                elif ((instruction&0x000f) == 6):
                    return 'lsr'
                elif ((instruction&0x000f) == 7):
                    return 'ror'
                elif ((instruction&0x000f) == 0xa):
                    return 'dec'
                elif ((instruction&0x000f) == 0xb):
                    return 'des'
                elif ((instruction&0x000e)>>1 == 6):
                    return 'jmp'
                elif ((instruction&0x000e)>>1 == 7):
                    return 'call'
                else:
                    return None
            elif ((instruction&0x0200)>>9 == 1):
                if ((instruction&0x0100)>>8 == 0):
                    return 'adiw'
                elif ((instruction&0x0100)>>8 == 1):
                    return 'sbiw'
                else:
                    return None
            else:
                return None
        elif ((instruction&0x0c00)>>10 == 2):
            if ((instruction&0x0300)>>8 == 0):
                return 'cbi'
            elif ((instruction&0x0300)>>8 == 1):
                return 'sbic'
            elif ((instruction&0x0300)>>8 == 2):
                return 'sbi'
            elif ((instruction&0x0300)>>8 == 3):
                return 'sbis'
            else:
                return None
        elif ((instruction&0x0c00)>>10 == 3):
            return 'mul'
        else:
            return None
    elif high_msn == 0xa:
        if ((instruction&0x0200) == 0):
            return 'ldd'
        elif ((instruction&0x0200) != 0):
            return 'std'
        else:
            return None

    elif high_msn == 0xb:
        if ((instruction&0x0800) == 0):
            return 'in'
        elif ((instruction&0x0800) != 1):
            return 'out'
        else:
            return None

    elif high_msn == 0xc:
        return 'rjmp'

    elif high_msn == 0xd:
        return 'rcall'

    elif high_msn == 0xe:
        return 'ldi'

    elif high_msn == 0xf:
        if ((instruction&0x0c00)>>10 == 0):
            if ((instruction&0x000f) == 0):
                return 'brcs'
                #return 'brlo' BRCS and BRLO are the same command
            elif ((instruction&0x0007) == 1):
                return 'breq'
            elif ((instruction&0x0007) == 2):
                return 'brmi'
            elif ((instruction&0x0007) == 3):
                return 'brvs'
            elif ((instruction&0x0007) == 4):
                return 'brlt'
            elif ((instruction&0x0007) == 5):
                return 'brhs'
            elif ((instruction&0x0007) == 6):
                return 'brts'
            elif ((instruction&0x0007) == 7):
                return 'brie'
            else:
                return 'brbs'
        elif ((instruction&0x0c00)>>10 == 1):
            if ((instruction&0x0007) == 0):
                return 'brcc'
                #return 'brsh' BRCC and BRSH are the same command
            elif ((instruction&0x0007) == 1):
                return 'brne'
            elif ((instruction&0x0007) == 2):
                return 'brpl'
            elif ((instruction&0x0007) == 3):
                return 'brvc'
            elif ((instruction&0x0007) == 4):
                return 'brge'
            elif ((instruction&0x0007) == 5):
                return 'brhc'
            elif ((instruction&0x0007) == 6):
                return 'brtc'
            elif ((instruction&0x0007) == 7):
                return 'brid'
            else:
                return 'brbc'
        elif ((instruction&0x0c00)>>10 == 2):
            if ((instruction&0x0200)>>9 == 0):
                return 'bld'
            elif ((instruction&0x0200)>>9 == 1):
                return 'bst'
            else:
                return None
        elif ((instruction&0x0c00)>>10 == 3):
            if ((instruction&0x0200)>>9 == 1):
                return 'sbrc'
            elif ((instruction&0x0200)>>9 == 0):
                return 'sbrs'
            else:
                return None
        else:
            return None

    else:
        return None


class AVR(Architecture):
    name = 'AVR'
    address_size = 2
    default_int_size = 2
    max_instr_length = 4
    regs = {
        'r0': RegisterInfo('r0', 1),
        'r1': RegisterInfo('r1', 1),
        'r2': RegisterInfo('r2', 1),
        'r3': RegisterInfo('r3', 1),
        'r4': RegisterInfo('r4', 1),
        'r5': RegisterInfo('r5', 1),
        'r6': RegisterInfo('r6', 1),
        'r7': RegisterInfo('r7', 1),
        'r8': RegisterInfo('r8', 1),
        'r9': RegisterInfo('r9', 1),
        'r10': RegisterInfo('r10', 1),
        'r11': RegisterInfo('r11', 1),
        'r12': RegisterInfo('r12', 1),
        'r13': RegisterInfo('r13', 1),
        'r14': RegisterInfo('r14', 1),
        'r15': RegisterInfo('r15', 1),
        'r16': RegisterInfo('r16', 1),
        'r17': RegisterInfo('r17', 1),
        'r18': RegisterInfo('r18', 1),
        'r19': RegisterInfo('r19', 1),
        'r20': RegisterInfo('r20', 1),
        'r21': RegisterInfo('r21', 1),
        'r22': RegisterInfo('r22', 1),
        'r23': RegisterInfo('r23', 1),
        'r24': RegisterInfo('r24', 1),
        'r25': RegisterInfo('r25', 1),
        'r26': RegisterInfo('r26', 1),
        'r27': RegisterInfo('r27', 1),
        'r28': RegisterInfo('r28', 1),
        'r29': RegisterInfo('r29', 1),
        'r30': RegisterInfo('r30', 1),
        'r31': RegisterInfo('r31', 1)
    }
    stack_pointer = 'SP'
    flags = ['C', 'Z', 'N', 'V', 'S', 'H', 'T', 'I']
    flag_write_types =['*', 'onlyT', 'svnz', 'onlyC', 'onlyH', 'onlyI', 'onlyN', 'onlyS', 'onlyV', 'onlyZ', 'svnzc', 'hsvnzc', 'zc']
    flags_written_by_flag_write_type = {
        '*' : ['C', 'Z', 'N', 'V', 'S', 'H', 'T', 'I'],
        'onlyT' : ['T'],
        'svnz' : ['S', 'V', 'N', 'Z'],
        'onlyC' : ['C'],
        'onlyH' : ['H'],
        'onlyI' : ['I'],
        'onlyN' : ['N'],
        'onlyS' : ['S'],
        'onlyV' : ['V'],
        'onlyZ' : ['Z'],
        'svnzc' : ['S', 'V', 'N', 'Z', 'C'],
        'hsvnzc' : ['H', 'S', 'V', 'N', 'Z', 'C'],
        'zc' : ['Z', 'C']
    }
    flag_roles = {
        'C': enums.FlagRole.CarryFlagRole,
        'Z': enums.FlagRole.ZeroFlagRole,
        'N': enums.FlagRole.NegativeSignFlagRole,
        'V': enums.FlagRole.OverflowFlagRole,
        'S': enums.FlagRole.SpecialFlagRole, #TODO
        'H': enums.FlagRole.SpecialFlagRole, #TODO
        'T': enums.FlagRole.SpecialFlagRole, #TODO
        'I': enums.FlagRole.SpecialFlagRole #TODO
    }
    # flags_required_for_flag_condition = {
    #     LLFC_E : ['Z'], #Equal
    #     LLFC_NE : ['Z'], #Not Equal
    #     LLFC_SLT : ['N'], #Signed Less Than
    #     LLFC_ULT : [''], #Unsigned Less Than
    #     LLFC_SLE : ['N'], #Signed Less Then or Equal to
    #     LLFC_ULE : [''], #Unsigned Less Than or Equal to
    #     LLFC_SGE : ['N'], #Signed Greather Than
    #     LLFC_UGE : [''], #Unsigned Greater Than
    #     LLFC_SGT : ['N'], #Signed Greater Than
    #     LLFC_UGT : ['C'], #Unsigned Greater Than
    #     LLFC_NEG : ['N'], #Negative
    #     LLFC_POS : ['N'], #Positive
    #     LLFC_O : ['V'], #Overflow
    #     LLFC_NO : ['V'] #No Overflow
    # }

    def decode_instruction(self, data, addr):
        error_value = (None, None, None, None, None, None, None, None, None)
        if len(data) < 2:
            return error_value

        instruction = struct.unpack('<H', data[0:2])[0]

        #print("Current Instruction is " + str(hex(instruction)))

        if instruction == 0x95C8:
            return 'lpm', None, None, None, None, None, 2, None, None
        elif instruction == 0x95D8:
            return 'elpm', None, None, None, None, None, 2, None, None
        elif instruction == 0x0000:
            return 'nop', None, None, None, None, None, 2, None, None
        elif instruction == 0x9508:
            return 'ret', None, None, None, None, None, 2, None, None
        elif instruction == 0x9518:
            return 'reti', None, None, None, None, None, 2, None, None
        elif instruction == 0x9408:
            return 'sec', None, None, None, None, None, 2, None, None
        elif instruction == 0x9458:
            return 'seh', None, None, None, None, None, 2, None, None
        elif instruction == 0x9478:
            return 'sei', None, None, None, None, None, 2, None, None
        elif instruction == 0x9428:
            return 'sen', None, None, None, None, None, 2, None, None
        elif instruction == 0x9448:
            return 'ses', None, None, None, None, None, 2, None, None
        elif instruction == 0x9468:
            return 'set', None, None, None, None, None, 2, None, None
        elif instruction == 0x9438:
            return 'sev', None, None, None, None, None, 2, None, None
        elif instruction == 0x9418:
            return 'sez', None, None, None, None, None, 2, None, None
        elif instruction == 0x9588:
            return 'sleep', None, None, None, None, None, 2, None, None
        elif instruction == 0x95E8:
            return 'spm', None, None, None, None, None, 2, None, None
        elif instruction == 0x95F8: #TODO
            return 'spm z+', None, None, None, None, None, 2, None, None
        elif instruction == 0x95A8:
            return 'wdr', None, None, None, None, None, 2, None, None
        elif instruction == 0x9598:
            return 'break', None, None, None, None, None, 2, None, None
        elif instruction == 0x9488:
            return 'clc', None, None, None, None, None, 2, None, None
        elif instruction == 0x94D8:
            return 'clh', None, None, None, None, None, 2, None, None
        elif instruction == 0x94F8:
            return 'cli', None, None, None, None, None, 2, None, None
        elif instruction == 0x94A8:
            return 'cln', None, None, None, None, None, 2, None, None
        elif instruction == 0x94C8:
            return 'cls', None, None, None, None, None, 2, None, None
        elif instruction == 0x94E8:
            return 'clt', None, None, None, None, None, 2, None, None
        elif instruction == 0x94B8:
            return 'clv', None, None, None, None, None, 2, None, None
        elif instruction == 0x9498:
            return 'clz', None, None, None, None, None, 2, None, None
        elif instruction == 0x9519:
            return 'eicall', None, None, None, None, None, 2, None, None
        elif instruction == 0x9419:
            return 'eijmp', None, None, None, None, None, 2, None, None
        elif instruction == 0x9509:
            return 'icall', None, None, None, None, None, 2, None, None
        elif instruction == 0x9409:
            return 'ijmp', None, None, None, None, None, 2, None, None

        #High byte most significant nibble
        high_msn = (instruction&0xf000) >> 12
        #print("The high byte most significant nibble is : " + str(high_msn))

        instr = get_instr_name(instruction, high_msn)

        if instr is None:
            log_error('Bad opcode: {:x}'.format(instruction))
            return error_value

        if instr == 'sts' or instr == 'lds' or instr == 'call' or instr == 'jmp':
            width = 2
        else:
            width = None

        src, src_operand_type, dst, dst_operand_type = GetOperands(instr, instruction)

        if width != None:
            length = 2 + width
        else:
            length = 2

        if length == 4:
            direct_addr = struct.unpack('<H', data[2:4])[0]
            if instr == 'sts':
                dst = direct_addr
            elif instr == 'lds':
                src = direct_addr
            elif instr == 'call':
                dst = direct_addr
            elif instr == 'jmp':
                dst = direct_addr

        src_value, dst_value = None, None

        return instr, width, src_operand_type, dst_operand_type, src, dst, length, src_value, dst_value


    def perform_get_instruction_info(self, data, addr):
        instr, _, _, _, _, dst, length, src_value, _ = self.decode_instruction(data, addr)

        if instr is None:
            return None

        result = InstructionInfo()
        result.length = length

        if instr == 'ret':
            result.add_branch(BranchType.FunctionReturn)
        elif instr == 'reti':
            result.add_branch(BranchType.FunctionReturn)
        elif instr == 'call':
            result.add_branch(BranchType.CallDestination, dst*2)
        elif instr == 'rcall':
            result.add_branch(BranchType.CallDestination, addr + dst*2 + 1*2)
        elif instr == 'jmp':
            result.add_branch(BranchType.UnconditionalBranch, dst*2)
        elif instr == 'rjmp':
            result.add_branch(BranchType.UnconditionalBranch, addr + dst*2 + 1*2)
        elif (instr == 'breq' or instr == 'brne' or instr == 'brcs'
                or instr == 'brcc' or instr == 'brsh' or instr == 'brlo'
                or instr == 'brmi' or instr == 'brpl' or instr == 'brge'
                or instr == 'brlt' or instr == 'brhs' or instr == 'brhc'
                or instr == 'brts' or instr == 'brtc' or instr == 'brvs'
                or instr == 'brvc' or instr == 'brie' or instr == 'brid'):
            result.add_branch(BranchType.TrueBranch, addr + dst*2 + 1*2)
            result.add_branch(BranchType.FalseBranch, addr + 1*2)
        elif (instr == 'brbs' or instr == 'brbc'):
            result.add_branch(BranchType.TrueBranch, addr + dst*2 + 1*2)
            result.add_branch(BranchType.FalseBranch, addr + 1*2)
        elif (instr == 'cpse' or instr == 'sbrc' or instr == 'sbrs'
                or instr == 'sbic' or instr == 'sbis'):
            result.add_branch(BranchType.TrueBranch, addr + 2*2)
            result.add_branch(BranchType.FalseBranch, addr + 1*2)
        elif (instr == 'icall' or instr == 'ijmp'):
            result.add_branch(BranchType.IndirectBranch)

        #TODO

        return result


    def perform_get_instruction_text(self, data, addr):
        instr, width, src_operand_type, dst_operand_type, src, dst, length, src_value, dst_value = self.decode_instruction(data, addr)

        if instr is None:
            return None

        tokens = []

        instruction_text = instr

        tokens = [
            InstructionTextToken(InstructionTextTokenType.TextToken, '{:7s}'.format(instruction_text))
        ]

        if dst_operand_type != None:
            tokens += OperandTokenGen[dst_operand_type](dst, addr, instr)
        #
        if dst_operand_type != None and src_operand_type != None:
            tokens += [InstructionTextToken(InstructionTextTokenType.TextToken, ',')]
        #
        if src_operand_type != None:
            tokens += OperandTokenGen[src_operand_type](src, addr, instr)

        return tokens, length

    #TODO
    def perform_get_instruction_low_level_il(self, data, addr, il):
        return
    def perform_get_flag_write_low_level_il(self, op, size, write_type, flag, operands, il):
        return
    def perform_get_flag_condition_low_level_il(self, cond, il):
        return


AVR.register()
BinaryViewType['ELF'].register_arch(83, Endianness.LittleEndian, Architecture["AVR"])