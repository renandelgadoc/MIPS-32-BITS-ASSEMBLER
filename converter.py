def tipoR(instrucao,comando):
    operacao = instrucao[0]
    opCodeX = 0
    chamtX = 0
    function = funct[operacao]
    if instrucao[0] == 'sll' or instrucao[0] == 'srl' or instrucao[0] == 'sra':
        rs = 'zero'
        rd = instrucao[1][1:3]
        rt = instrucao[2][1:3]
        chamtX = int(instrucao[3])
    elif instrucao[0] == 'mult' or instrucao[0] == 'div':
        rd = 'zero'
        rs = instrucao[1][1:3]
        rt = instrucao[2][1:3]
    elif instrucao[0] == 'mfhi' or instrucao[0] == 'mflo':
        rt = 'zero'
        rs = 'zero'
        rd = instrucao[1][1:3]
    elif instrucao[0] == 'srav':
        rd = instrucao[1][1:3]
        rt = instrucao[2][1:3]
        rs = instrucao[3][1:3]
    elif instrucao[0] == 'jr':
        rt = 'zero'
        rd = 'zero'
        rs = instrucao[1][1:3]
    elif instrucao[0] == 'jalr':
        rt = 'zero'
        rd = 'ra'
        rs = instrucao[1][1:3]
        if len(instrucao) > 2:
            rd = instrucao[1][1:3]
            rs = instrucao[2][1:3]
    else:
        rd = instrucao[1][1:3]
        rs = instrucao[2][1:3]
        rt = instrucao[3][1:3]
    return ("{:06b}".format(opCodeX) +
            "{:05b}".format(registers[rs]) +
            "{:05b}".format(registers[rt]) +
            "{:05b}".format(registers[rd]) +
            "{:05b}".format(chamtX) +
            "{:06b}".format(function))

def tipoI(instrucao,comando):
    if (comando.count(",") == 2):
        operacao, rt, rs, imm = instrucao
        binario = ("{:06b}".format(opCode[operacao]) +
                   "{:05b}".format(registers[rs[1:3]]) +
                   "{:05b}".format(registers[rt[1:3]]) +
                   "{:016b}".format(int(imm)))
        return binario
    operacao, rt, imm_rs = instrucao
    imm, rs = imm_rs[:-1].split("(")
    binario = ("{:06b}".format(opCode[operacao]) +
               "{:05b}".format(registers[rs[1:]]) +
               "{:05b}".format(registers[rt[1:3]]) +
               "{:016b}".format(int(imm)))
    return binario

def tipoJ(instrucao,comando):
    return

def tipoFMT(instrucao,comando):
    operacao = instrucao[0]
    opCodeX = 17
    if operacao.split('.')[0] == 'c':
        operacao = operacao.replace('eq.',"")
        fs = int(instrucao[1][2:3])
        ft = int(instrucao[2][2:3])
        cc = '000'
        cond ='0010'
        fd = int(cc + '00',2)
        function = int('11' + cond,2)
    else:
        ft = int(instrucao[3][2:3])
        fs = int(instrucao[2][2:3])
        fd = int(instrucao[1][2:3])
        function = functFMT[operacao.split('.')[0]]
    if operacao.split('.')[1] == 'd':
        fmt = 17
    else:
        fmt = 16
    return("{:06b}".format(opCodeX) +
            "{:05b}".format(fmt) +
            "{:05b}".format(ft) +
            "{:05b}".format(fs) +
            "{:05b}".format(fd) +
            "{:06b}".format(function))

registers = {
    'zero': 0,   'at': 1,   'v0': 2,   'v1': 3,
    'a0': 4,   'a1': 5,   'a2': 6,   'a3': 7,
    't0': 8,   't1': 9,   't2': 10,  't3': 11,
    't4': 12,  't5': 13,  't6': 14,  't7': 15,
    's0': 16,  's1': 17,  's2': 18,  's3': 19,
    's4': 20,  's5': 21,  's6': 22,  's7': 23,
    't8': 24,  't9': 25,  'k0': 26,  'k1': 27,
    'gp': 28,  'sp': 29,  'fp': 30,  'ra': 31
}

opCode = {
    'lw': 35, 'sw': 43, 'beq': 4, 'j': 2, 'xori': 14, 'lb': 32,
}

funct = {
    'add': 32, 'addu': 33, 'sub': 34, 'subu': 35, 'xor': 38, 'sll': 0, 'srl': 2, 'and': 36,
    'slt': 42, 'or': 37, 'nor': 39, 'mult': 24, 'div': 26, 'mfhi': 16, 'mflo': 18, 'sra': 3,
    'srav': 7, 'sltu': 43, 'jr': 8, 'jalr': 9
}

functFMT = {
    'add': 0, 'sub': 1, 'mul': 2, 'div': 3
}

instructionsType = {
    'add': tipoR, 'addu': tipoR, 'sub': tipoR, 'subu': tipoR, 'xor': tipoR, 'sll': tipoR,
    'srl': tipoR, 'and': tipoR, 'or': tipoR, 'nor': tipoR, 'slt': tipoR, 'mult': tipoR,
    'div': tipoR, 'mfhi': tipoR, 'mflo': tipoR, 'sra': tipoR, 'srav': tipoR, 'sltu': tipoR,
    'jr': tipoR, 'jalr': tipoR,

    'lw': tipoI, 'sw': tipoI, 'beq': tipoI, 'xori': tipoI, 'lb': tipoI,

    'j': tipoJ,
    
    'add.d': tipoFMT, 'add.s': tipoFMT, 'sub.d': tipoFMT, 'sub.s': tipoFMT,
    'c.eq.d': tipoFMT, 'c.eq.s': tipoFMT, 'mul.d': tipoFMT, 'mul.s': tipoFMT,
    'div.d': tipoFMT, 'div.s': tipoFMT
}


with open('input.txt') as entrada:
    listaComandos = entrada.readlines()
    i = 0
    for comando in listaComandos:
        instrucao = comando.strip('\n').split(" ")
        convertido = instructionsType[instrucao[0]](instrucao,comando)
        print("{0:08x} : {1:08x} ; % {2} %".format(i, int(convertido, 2), comando.strip('\n')))
        i = i + 1