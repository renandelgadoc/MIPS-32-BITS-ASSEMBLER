def tipoR(instrucao,comando):
    operacao = instrucao[0]
    opCodeX = 0
    chamtX = 0
    function = funct[operacao]
    if instrucao[0] == 'sll' or instrucao[0] == 'srl':
        rs = 'zero'
        rd = instrucao[1][1:3]
        rt = instrucao[2][1:3]
        chamtX = int(instrucao[3])
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
    'add': 0, 'sub': 0, 'xor': 0, 'lw': 35, 'sw': 43, 'beq': 4, 'j': 2, 'xori': 14, 'lb': 32, 'sll': 0,
}

chamt = {
    'add': 0, 'sub': 0, 'xor': 0,
}

funct = {
    'add': 32, 'sub': 34, 'xor': 38, 'sll': 0, 'srl': 2
}

instructionsType = {
    'add': tipoR, 'sub': tipoR, 'xor': tipoR, 'sll': tipoR, 'srl': tipoR,

    'lw': tipoI, 'sw': tipoI, 'beq': tipoI, 'xori': tipoI, 'lb': tipoI,

    'j': tipoJ
}


with open('input.txt') as entrada:
    listaComandos = entrada.readlines()
    i = 0
    for comando in listaComandos:
        instrucao = comando.strip('\n').split(" ")
        convertido = instructionsType[instrucao[0]](instrucao,comando)
        print("{0:08x} : {1:08x} ; % {2} %".format(i, int(convertido, 2), comando.strip('\n')))
        i = i + 1