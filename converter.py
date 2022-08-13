registers = {
    'zero': 0, 'at': 1, 'v0': 2, 'v1': 3,
    'a0': 4, 'a1': 5, 'a2': 6, 'a3': 7,
    't0': 8, 't1': 9, 't2': 10, 't3': 11,
    't4': 12, 't5': 13, 't6': 14, 't7': 15,
    's0': 16, 's1': 17, 's2': 18, 's3': 19,
    's4': 20, 's5': 21, 's6': 22, 's7': 23,
    't8': 24, 't9': 25, 'k0': 26, 'k1': 27,
    'gp': 28, 'sp': 29, 'fp': 30, 'ra': 31
}

opCode = {
    'tipo_r': 0, 'bgez': 1, 'bgezal': 1, 'j': 2, 'jal': 3, 'beq': 4, 'bne': 5, 'addi': 8, 'addiu': 9, 'slti': 10,
    'sltiu': 11,
    'andi': 12,
    'ori': 13, 'xori': 14, 'lui': 15, 'lb': 32, 'sb': 38, 'lw': 35, 'sw': 43
}

funct = {
    'add': 32, 'addu': 33, 'sub': 34, 'subu': 35, 'xor': 38, 'sll': 0, 'srl': 2, 'and': 36,
    'slt': 42, 'or': 37, 'nor': 39, 'mult': 24, 'div': 26, 'mfhi': 16, 'mflo': 18, 'sra': 3,
    'srav': 7, 'sltu': 43, 'jr': 8, 'jalr': 9
}

rt_code = {
    'bgez': 1, 'bgezal': 17,
}

functFMT = {
    'add': 0, 'sub': 1, 'mul': 2, 'div': 3
}

labels = {}


def tipo_r(lista_de_parametros):
    operacao = lista_de_parametros[0]
    op_code_x = opCode['tipo_r']
    chamt_x = 0
    function = funct[operacao]
    if lista_de_parametros[0] == 'sll' or lista_de_parametros[0] == 'srl' or lista_de_parametros[0] == 'sra':
        rs = 'zero'
        rd = lista_de_parametros[1].replace('$', '').replace(',', '')
        rt = lista_de_parametros[2].replace('$', '').replace(',', '')
        chamt_x = int(lista_de_parametros[3])
    elif lista_de_parametros[0] == 'mult' or lista_de_parametros[0] == 'div':
        rd = 'zero'
        rs = lista_de_parametros[1].replace('$', '').replace(',', '')
        rt = lista_de_parametros[2].replace('$', '').replace(',', '')
    elif lista_de_parametros[0] == 'mfhi' or lista_de_parametros[0] == 'mflo':
        rt = 'zero'
        rs = 'zero'
        rd = lista_de_parametros[1].replace('$', '').replace(',', '')
    elif lista_de_parametros[0] == 'srav':
        rd = lista_de_parametros[1].replace('$', '').replace(',', '')
        rt = lista_de_parametros[2].replace('$', '').replace(',', '')
        rs = lista_de_parametros[3].replace('$', '').replace(',', '')
    elif lista_de_parametros[0] == 'jr':
        rt = 'zero'
        rd = 'zero'
        rs = lista_de_parametros[1].replace('$', '').replace(',', '')
    elif lista_de_parametros[0] == 'jalr':
        rt = 'zero'
        rd = 'ra'
        rs = lista_de_parametros[1].replace('$', '').replace(',', '')
        if len(lista_de_parametros) > 2:
            rd = lista_de_parametros[1].replace('$', '').replace(',', '')
            rs = lista_de_parametros[2].replace('$', '').replace(',', '')
    else:
        rd = lista_de_parametros[1].replace('$', '').replace(',', '')
        rs = lista_de_parametros[2].replace('$', '').replace(',', '')
        rt = lista_de_parametros[3].replace('$', '').replace(',', '')
    return ("{:06b}".format(op_code_x)
            + "{:05b}".format(registers[rs])
            + "{:05b}".format(registers[rt])
            + "{:05b}".format(registers[rd])
            + "{:05b}".format(chamt_x)
            + "{:06b}".format(function))


def transforma_negativo_em_complemento_de_2(imm):
    imm = list(imm)
    for i in range(0, len(imm)):
        imm[i] = '0' if imm[i] == '1' else '1'
    return ''.join(imm)


def tipo_i(lista_de_parametros):
    # identifica se a instrução usa immediate e separa cria uma lista com a intrução
    if lista_de_parametros[0] == "bgez" or lista_de_parametros[0] == "bgezal":
        operacao, rs, imm = lista_de_parametros
        rt = rt_code[operacao]
        rs = registers[rs.replace('$', '').replace(',', '')]
        imm = labels[imm]
    elif lista_de_parametros[0] == "beq" or lista_de_parametros[0] == "bne":
        operacao, rs, rt, imm = lista_de_parametros
        rt = registers[rt.replace('$', '').replace(',', '')]
        rs = registers[rs.replace('$', '').replace(',', '')]
        imm = labels[imm]
    elif len(lista_de_parametros) == 3:
        operacao, rt, var = lista_de_parametros
        imm, rs = var[:-1].split("(")
        rs = registers[rs.replace('$', '').replace(',', '')]
        rt = registers[rt.replace('$', '').replace(',', '')]
    else:
        operacao, rt, rs, imm = lista_de_parametros
        rs = registers[rs.replace('$', '').replace(',', '')]
        rt = registers[rt.replace('$', '').replace(',', '')]
    # transforma o immediate em binário complemento de 2
    imm = int(imm)
    if imm < 0:
        imm = transforma_negativo_em_complemento_de_2("{:016b}".format((imm * -1) - 1))
    else:
        imm = "{:016b}".format(imm)
    # retorna a word
    return ("{:06b}".format(opCode[operacao])
            + "{:05b}".format(rs)
            + "{:05b}".format(rt)
            + imm)


def tipo_j(lista_de_parametros):
    operacao = lista_de_parametros[0]
    label = labels[lista_de_parametros[1]]
    return ("{:06b}".format(opCode[operacao])
            + "{:026b}".format(label))


def tipo_fmt(lista_de_parametros):
    operacao = lista_de_parametros[0]
    op_code_x = 17
    if operacao.split('.')[0] == 'c':
        operacao = operacao.replace('eq.', "")
        fs = int(lista_de_parametros[1][2:3])
        ft = int(lista_de_parametros[2][2:3])
        cc = '000'
        cond = '0010'
        fd = int(cc + '00', 2)
        function = int('11' + cond, 2)
    else:
        ft = int(lista_de_parametros[3][2:3])
        fs = int(lista_de_parametros[2][2:3])
        fd = int(lista_de_parametros[1][2:3])
        function = functFMT[operacao.split('.')[0]]
    if operacao.split('.')[1] == 'd':
        fmt = 17
    else:
        fmt = 16
    return ("{:06b}".format(op_code_x)
            + "{:05b}".format(fmt)
            + "{:05b}".format(ft)
            + "{:05b}".format(fs)
            + "{:05b}".format(fd)
            + "{:06b}".format(function))


instructionsType = {
    'add': tipo_r, 'addu': tipo_r, 'sub': tipo_r, 'subu': tipo_r, 'xor': tipo_r, 'sll': tipo_r,
    'srl': tipo_r, 'and': tipo_r, 'or': tipo_r, 'nor': tipo_r, 'slt': tipo_r, 'mult': tipo_r,
    'div': tipo_r, 'mfhi': tipo_r, 'mflo': tipo_r, 'sra': tipo_r, 'srav': tipo_r, 'sltu': tipo_r,
    'jr': tipo_r, 'jalr': tipo_r,

    'lw': tipo_i, 'sw': tipo_i, 'beq': tipo_i, 'bne': tipo_i, 'xori': tipo_i, 'lb': tipo_i, 'sb': tipo_i,
    'addi': tipo_i,
    'addiu': tipo_i, 'andi': tipo_i, 'ori': tipo_i, 'lui': tipo_i, 'slti': tipo_i, 'sltiu': tipo_i, 'bgez': tipo_i,
    'bgezal': tipo_i,

    'j': tipo_j, 'jal': tipo_j,

    'add.d': tipo_fmt, 'add.s': tipo_fmt, 'sub.d': tipo_fmt, 'sub.s': tipo_fmt,
    'c.eq.d': tipo_fmt, 'c.eq.s': tipo_fmt, 'mul.d': tipo_fmt, 'mul.s': tipo_fmt,
    'div.d': tipo_fmt, 'div.s': tipo_fmt
}
# limpa o arquivo de output para a próxima execução
with open('output_text.txt', 'w'):
    pass

with open('input.txt') as entrada:
    listaComandos = entrada.readlines()
    iText = 0
    iData = 0
    for linha in listaComandos:
        if linha == '\n':
            print()
            continue
        elif linha == '.data\n' or linha == '.text\n':
            campo = linha
            continue
        if campo == '.data\n':
            words = linha.replace(',', "").strip('\n').split(" ")[2:]
            for word in words:
                print("{0:08x} : {1:08x};".format(iData, int(word, 16)))
                with open('output_data.txt', 'a') as saidaData:
                    saidaData.write("{0:08x} : {1:08x};\n".format(iData, int(word, 16)))
                    saidaData.close()
                iData += 1
        elif campo == '.text\n':
            instrucao = linha.strip('\n').split(" ")
            if ':' in instrucao[0]:
                labels[instrucao[0][:-1]] = iText
                instrucao.pop(0)
            convertido = instructionsType[instrucao[0]](instrucao)
            print("{0:08x} : {1:08x} ; % {2} %".format(iText, int(convertido, 2), linha.strip('\n')))
            with open('output_text.txt', 'a') as saidaText:
                saidaText.write("{0:08x} : {1:08x} ; % {2} %\n".format(iText, int(convertido, 2), linha.strip('\n')))
            iText += 1
