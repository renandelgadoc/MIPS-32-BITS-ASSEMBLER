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
    'tipo_r': 0, 'bgez': 1, 'bgezal': 1, 'j': 2, 'jal': 3, 'beq': 4, 'bne': 5, 'addi': 8, 'addiu': 9, 'li': 9,  'slti': 10,
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


def tipo_r(lista_de_parametros, numero_linha):
    global linha
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
    escrever_output("{:06b}".format(op_code_x)
                    + "{:05b}".format(registers[rs])
                    + "{:05b}".format(registers[rt])
                    + "{:05b}".format(registers[rd])
                    + "{:05b}".format(shamt_x)
                    + "{:06b}".format(function), linha, numero_linha)
    return


def tipo_r2(lista_de_parametros, numero_linha):
    global linha
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
    escrever_output("{:06b}".format(op_code_x)
                    + "{:05b}".format(registers[rs])
                    + "{:05b}".format(registers[rt])
                    + "{:05b}".format(registers[rd])
                    + "{:05b}".format(shamt_x)
                    + "{:06b}".format(function), linha, numero_linha)
    return


def transforma_negativo_em_complemento_de_2(imm):
    if imm > 0:
        return '{:032b}'.format(imm)
    imm = (imm * -1) - 1
    imm = '{:032b}'.format(imm)
    imm = list(imm)
    for i in range(0, len(imm)):
        imm[i] = '0' if imm[i] == '1' else '1'
    return ''.join(imm)


def branch_target_adress(label):
    bta = labels[label] - (i_text + 1)
    return bta

def converte_string_para_inteiro(n):
    if 'x' in n:
        return int(n, 16)
    return int(n)

def tipo_i(lista_de_parametros, numero_linha):
    global linha
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
        if lista_de_parametros[0] == 'lui' or lista_de_parametros[0] == 'li':
            rs = registers['zero']
            operacao, rt, imm = lista_de_parametros
            rt = registers[rt]
        else:
            operacao, rt, var = lista_de_parametros
            imm, rs = var[:-1].split("(")
            rs = registers[rs]
            rt = registers[rt]
        imm = converte_string_para_inteiro(imm)
    else:
        operacao, rt, rs, imm = lista_de_parametros
        rs = registers[rs]
        rt = registers[rt]
        imm = converte_string_para_inteiro(imm)

    # transforma o immediate em binário complemento de 2

    imm_bin = transforma_negativo_em_complemento_de_2(imm)

    imm_mais_significativo, imm_menos_significativo = imm_bin[:16], imm_bin[16:]

    if abs(imm) > 65535:
        escrever_output("{:06b}".format(opCode['lui'])
                        + "{:05b}".format(registers['zero'])
                        + "{:05b}".format(registers['at'])
                        + imm_mais_significativo, linha, numero_linha)
        if operacao == 'li':
            escrever_output("{:06b}".format(opCode['ori'])
                            + "{:05b}".format(registers['at'])
                            + "{:05b}".format(rt)
                            + imm_menos_significativo, "", numero_linha)
            return
        escrever_output("{:06b}".format(opCode['ori'])
                        + "{:05b}".format(registers['at'])
                        + "{:05b}".format(registers['at'])
                        + imm_menos_significativo, "", numero_linha)
        lista_valores = list(registers.keys())
        linha = ""
        tipo_r([operacao.replace('i', ''), lista_valores[list(registers.values()).index(rt)], lista_valores[list(registers.values()).index(rs)], "at"], numero_linha)
        return
    escrever_output("{:06b}".format(opCode[operacao])
                    + "{:05b}".format(rs)
                    + "{:05b}".format(rt)
                    + imm_menos_significativo, linha, numero_linha)

    return


def tipo_j(lista_de_parametros, numero_linha):
    global linha
    operacao = lista_de_parametros[0]
    label = labels[lista_de_parametros[1]]
    escrever_output("{:06b}".format(opCode[operacao])
                    + "{:026b}".format(label), linha, numero_linha)


def tipo_fmt(lista_de_parametros, numero_linha):
    global linha
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
    escrever_output("{:06b}".format(op_code_x)
                    + "{:05b}".format(fmt)
                    + "{:05b}".format(ft)
                    + "{:05b}".format(fs)
                    + "{:05b}".format(fd)
                    + "{:06b}".format(function), linha, numero_linha)
    return


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


def escrever_output(sla, linha, numero_linha):
    global i_text
    if linha != "":
        linha = ("% " + str(numero_linha) + ': ' + linha + " %").replace('\n', '')
    print("{0:08x} : {1:08x} ; {2}".format(i_text, int(sla, 2), linha))
    with open('input_text.mif', 'a') as saida_text:
        saida_text.write("{0:08x} : {1:08x};  {2}\n".format(i_text, int(sla, 2), linha))
    i_text += 1

# limpa o arquivo de output para a próxima execução
with open('input_text.mif', 'w') as arquivo_text:
    arquivo_text.write('DEPTH = 4096;\n')
    arquivo_text.write('WIDTH = 32;\n')
    arquivo_text.write('ADDRESS_RADIX = HEX;\n')
    arquivo_text.write('DATA_RADIX = HEX;\n')
    arquivo_text.write('CONTENT\n')
    arquivo_text.write('BEGIN\n')
    arquivo_text.write('\n')
    pass
with open('input_data.mif', 'w') as arquivo_data:
    arquivo_data.write('DEPTH = 16384;\n')
    arquivo_data.write('WIDTH = 32;\n')
    arquivo_data.write('ADDRESS_RADIX = HEX;\n')
    arquivo_data.write('DATA_RADIX = HEX;\n')
    arquivo_data.write('CONTENT\n')
    arquivo_data.write('BEGIN\n')
    arquivo_data.write('\n')
    pass

# globais
i_data = 0
i_text = 0
with open('input.asm') as entrada:
    listaComandos = entrada.readlines()
    #   grava as labels em um dicionário
    for numero_linha, linha in enumerate(listaComandos):
        linha = linha.replace('$', '').replace(',', ' ').replace('\t', '').replace('\r', '').strip('\n').strip(" ")
        if linha == '':
            continue
        elif linha == '.data' or linha == '.text':
            campo = linha
            continue
        if campo == '.text':
            primeiro_elemento = linha.split(" ")[0]
            if ":" in primeiro_elemento:
                labels[primeiro_elemento.replace(':', '')] = int(i_text)
            i_text += 1
            if 'li' in linha or 'la' in linha:
                i_text += 1
    i_text = 0
    i_data = 0
    for numero_linha, linha in enumerate(listaComandos):
        numero_linha += 1
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
            word_armazenar = [nome_word, hex(i_data)]
            words_nome.append(nome_word)
            for elemento in linha_word[1:]:
                word_armazenar.append(int(elemento, 16))
            words_data.append(word_armazenar)
            words = linha_formatada.split(" ")[2:]
            for word in words:
                print("{0:08x} : {1:08x};".format(i_data, int(word, 16)))
                with open('input_data.mif', 'a') as saida_data:
                    saida_data.write("{0:08x} : {1:08x};\n".format(int(i_data/4), int(word, 16)))
                i_data += 4
        elif campo == '.text':
            instrucao = linha_formatada.split(" ")
            if ':' in instrucao[0]:
                instrucao.pop(0)
            if instrucao[0] == 'la':
                if instrucao[2] in words_nome:
                    data_endereco = words_data[words_nome.index(instrucao[2])][1]
                else:
                    continue
                tipo_i(['lui', 'at', '0x00001001'], numero_linha)
                i_text += 1
                linha = ''
                tipo_i(['ori', instrucao[1], 'at', data_endereco], numero_linha)
                i_text += 1
                continue
            else:
                instructionsType[instrucao[0]](instrucao, numero_linha)
    with open('input_text.mif', 'a') as saida_text:
        saida_text.write('\n')
        saida_text.write('END;\n')
    with open('input_data.mif', 'a') as saida_data:
        saida_data.write('\n')
        saida_data.write('END;\n')
