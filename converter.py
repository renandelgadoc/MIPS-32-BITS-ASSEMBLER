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
    'ori': 13, 'xori': 14, 'lui': 15, 'lb': 32, 'sb': 38, 'lw': 35, 'sw': 43,
    'tipo_r2': 28
}

funct = {
    'add': 32, 'addu': 33, 'sub': 34, 'subu': 35, 'xor': 38, 'sll': 0, 'srl': 2, 'and': 36,
    'slt': 42, 'or': 37, 'nor': 39, 'mult': 24, 'div': 26, 'mfhi': 16, 'mflo': 18, 'sra': 3,
    'srav': 7, 'sltu': 43, 'jr': 8, 'jalr': 9, 'clo': 33, 'madd': 0, 'msubu': 5, 'mul': 2, 'movn': 11
}

rt_code = {
    'bgez': 1, 'bgezal': 17,
}

functFMT = {
    'add': 0, 'sub': 1, 'mul': 2, 'div': 3
}

labels = {}
words_data = []
words_nome = []


def tipo_r(lista_de_parametros):
    operacao = lista_de_parametros[0]
    op_code_x = opCode['tipo_r']
    shamt_x = 0
    function = funct[operacao]
    if lista_de_parametros[0] == 'sll' or lista_de_parametros[0] == 'srl' or lista_de_parametros[0] == 'sra':
        rs = 'zero'
        rd = lista_de_parametros[1]
        rt = lista_de_parametros[2]
        shamt_x = int(lista_de_parametros[3])
    elif lista_de_parametros[0] == 'mult' or lista_de_parametros[0] == 'div':
        rd = 'zero'
        rs = lista_de_parametros[1]
        rt = lista_de_parametros[2]
    elif lista_de_parametros[0] == 'mfhi' or lista_de_parametros[0] == 'mflo':
        rt = 'zero'
        rs = 'zero'
        rd = lista_de_parametros[1]
    elif lista_de_parametros[0] == 'srav':
        rd = lista_de_parametros[1]
        rt = lista_de_parametros[2]
        rs = lista_de_parametros[3]
    elif lista_de_parametros[0] == 'jr':
        rt = 'zero'
        rd = 'zero'
        rs = lista_de_parametros[1]
    elif lista_de_parametros[0] == 'jalr':
        rt = 'zero'
        rd = 'ra'
        rs = lista_de_parametros[1]
        if len(lista_de_parametros) > 2:
            rd = lista_de_parametros[1]
            rs = lista_de_parametros[2]
    elif lista_de_parametros[0] == 'clo':
        rd = lista_de_parametros[1]
        rs = lista_de_parametros[2]
        rt = 'zero'
        op_code_x = 28
    else:
        rd = lista_de_parametros[1]
        rs = lista_de_parametros[2]
        rt = lista_de_parametros[3]
    return ("{:06b}".format(op_code_x)
            + "{:05b}".format(registers[rs])
            + "{:05b}".format(registers[rt])
            + "{:05b}".format(registers[rd])
            + "{:05b}".format(shamt_x)
            + "{:06b}".format(function))


def tipo_r2(lista_de_parametros):
    operacao = lista_de_parametros[0]
    op_code_x = opCode['tipo_r2']
    shamt_x = 0
    function = funct[operacao]
    if lista_de_parametros[0] == 'clo':
        rd = lista_de_parametros[1]
        rs = lista_de_parametros[2]
        rt = 'zero'
    elif len(lista_de_parametros) > 3:
        rd = lista_de_parametros[1]
        rs = lista_de_parametros[2]
        rt = lista_de_parametros[3]
    else:
        rd = 'zero'
        rs = lista_de_parametros[1]
        rt = lista_de_parametros[2]
    return ("{:06b}".format(op_code_x)
            + "{:05b}".format(registers[rs])
            + "{:05b}".format(registers[rt])
            + "{:05b}".format(registers[rd])
            + "{:05b}".format(shamt_x)
            + "{:06b}".format(function))


def transforma_negativo_em_complemento_de_2(imm):
    imm = list(imm)
    for i in range(0, len(imm)):
        imm[i] = '0' if imm[i] == '1' else '1'
    return ''.join(imm)


def branch_target_adress(label):
    with open('input_text.mif') as output:
        ultima_linha = len(output.readlines())
    bta = labels[label] - (ultima_linha + 1)
    return str(bta)


def tipo_i(lista_de_parametros):
    # identifica se a instrução usa immediate e separa cria uma lista com a intrução
    if lista_de_parametros[0] == "bgez" or lista_de_parametros[0] == "bgezal":
        operacao, rs, label = lista_de_parametros
        rt = rt_code[operacao]
        rs = registers[rs]
        imm = branch_target_adress(label)
    elif lista_de_parametros[0] == "beq" or lista_de_parametros[0] == "bne":
        operacao, rs, rt, label = lista_de_parametros
        rt = registers[rt]
        rs = registers[rs]
        imm = branch_target_adress(label)
    elif len(lista_de_parametros) == 3:
        if lista_de_parametros[0] == 'lui':
            rs = registers['zero']
            operacao, rt, imm = lista_de_parametros
            rt = registers[rt]
        else:
            operacao, rt, var = lista_de_parametros
            imm, rs = var[:-1].split("(")
            rs = registers[rs]
            rt = registers[rt]
    else:
        operacao, rt, rs, imm = lista_de_parametros
        rs = registers[rs]
        rt = registers[rt]
        # transforma o immediate em binário complemento de 2
    if 'x' in imm:
        imm = int(imm, 16)
    else:
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
        fs = int(lista_de_parametros[1][1:])
        ft = int(lista_de_parametros[2][1:])
        cc = '000'
        cond = '0010'
        fd = int(cc + '00', 2)
        function = int('11' + cond, 2)
    else:
        ft = int(lista_de_parametros[3][1:])
        fs = int(lista_de_parametros[2][1:])
        fd = int(lista_de_parametros[1][1:])
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
    'jr': tipo_r, 'jalr': tipo_r, 'movn': tipo_r,

    'clo': tipo_r2, 'madd': tipo_r2, 'msubu': tipo_r2, 'mul': tipo_r2,

    'lw': tipo_i, 'sw': tipo_i, 'beq': tipo_i, 'bne': tipo_i, 'xori': tipo_i, 'lb': tipo_i, 'sb': tipo_i,
    'addi': tipo_i,
    'addiu': tipo_i, 'andi': tipo_i, 'ori': tipo_i, 'lui': tipo_i, 'slti': tipo_i, 'sltiu': tipo_i, 'bgez': tipo_i,
    'bgezal': tipo_i, 'li': tipo_i,

    'j': tipo_j, 'jal': tipo_j,

    'add.d': tipo_fmt, 'add.s': tipo_fmt, 'sub.d': tipo_fmt, 'sub.s': tipo_fmt,
    'c.eq.d': tipo_fmt, 'c.eq.s': tipo_fmt, 'mul.d': tipo_fmt, 'mul.s': tipo_fmt,
    'div.d': tipo_fmt, 'div.s': tipo_fmt
}
# limpa o arquivo de output para a próxima execução
with open('input_text.mif', 'w'):
    pass
with open('input_data.mif', 'w'):
    pass

with open('input.asm') as entrada:
    listaComandos = entrada.readlines()
    iText = 0
    #   grava as labels em um dicionário
    for linha in listaComandos:
        linha = linha.replace('$', '').replace(',', ' ').replace('\t', '').replace('\r', '').strip('\n').strip(" ")
        if linha == '':
            continue
        elif linha == '.data' or linha == '.text':
            campo = linha
            continue
        if campo == '.text':
            primeiro_elemento = linha.split(" ")[0]
            if ":" in primeiro_elemento:
                labels[primeiro_elemento.replace(':', '')] = int(iText)
            iText += 1
            if 'li' in linha:
                iText += 1
    iText = 0
    iData = 0
    for linha in listaComandos:
        linha_formatada = linha.replace('$', '').replace(',', ' ').replace('\t', '').replace('\r', '').strip(
            '\n').strip(" ")
        while "  " in linha_formatada:
            linha_formatada = linha_formatada.replace('  ', ' ')
        if linha_formatada == '':
            print()
            continue
        elif linha_formatada == '.data' or linha_formatada == '.text':
            campo = linha_formatada
            continue
        if campo == '.data':
            linha_word = linha_formatada.replace(':', '').replace('.word ', '').split(' ')
            nome_word = linha_word[0]
            word_armazenar = [nome_word]
            words_nome.append(nome_word)
            for elemento in linha_word[1:]:
                word_armazenar.append(int(elemento, 16))
            words_data.append(word_armazenar)
            words = linha_formatada.split(" ")[2:]
            for word in words:
                print("{0:08x} : {1:08x};".format(iData, int(word, 16)))
                with open('input_data.mif', 'a') as saidaData:
                    saidaData.write("{0:08x} : {1:08x};\n".format(iData, int(word, 16)))
                iData += 1
        elif campo == '.text':
            instrucao = linha_formatada.split(" ")
            if ':' in instrucao[0]:
                instrucao.pop(0)
            if instrucao[0] == 'li':
                imm = instrucao[2]
                if 'x' in imm:
                    imm = int(instrucao[2], 16)
                else:
                    imm = int(instrucao[2])
                imm_bin = '{:032b}'.format(imm)
                imm1 = str(int(imm_bin[0:16], 2))
                imm2 = str(int(imm_bin[16:32], 2))
                sla = tipo_i(['lui', 'at', imm1])
                print("{0:08x} : {1:08x} ; % {2} %".format(iText, int(sla, 2), linha.replace('\n', '')))
                with open('input_text.mif', 'a') as saidaText:
                    saidaText.write("{0:08x} : {1:08x} ; % {2} %\n".format(iText, int(sla, 2), linha.replace('\n', '')))
                iText += 1
                sla = tipo_i(['ori', instrucao[1], 'at', imm2])
                print("{0:08x} : {1:08x} ;\n".format(iText, int(sla, 2)))
                with open('input_text.mif', 'a') as saidaText:
                    saidaText.write(
                        "{0:08x} : {1:08x} ;\n".format(iText, int(sla, 2)))
                iText += 1
                continue
            sla = instructionsType[instrucao[0]](instrucao)
            print("{0:08x} : {1:08x} ; % {2} %".format(iText, int(sla, 2), linha.replace('\n', '')))
            with open('input_text.mif', 'a') as saidaText:
                saidaText.write("{0:08x} : {1:08x} ; % {2} %\n".format(iText, int(sla, 2), linha.replace('\n', '')))
            iText += 1
