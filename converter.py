import sys
import os

# Nome do arquivo de entrada pode ser especificado por argumento na hora de executar.
# Caso não seja feito isso, o mesmo poderá ser digitado pelo shell.
try:
    nome_arquivo = sys.argv[1]
except IndexError:
    nome_arquivo = input("Digite o nome do arquivo: ")

# Dicionário de registradores.
# Retorna o valor de acordo com o nome.
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

# Dicionário de opCodes.
# Retorna o valor de acordo com a instrução.
opCode = {
    'tipo_r': 0, 'bgez': 1, 'bgezal': 1, 'j': 2, 'jal': 3, 'beq': 4, 'bne': 5, 'addi': 8, 'addiu': 9, 'li': 9,
    'slti': 10,
    'sltiu': 11,
    'andi': 12,
    'ori': 13, 'xori': 14, 'lui': 15, 'lb': 32, 'sb': 38, 'lw': 35, 'sw': 43,
    'tipo_r2': 28
}

# Dicionário de instruções.
# Retorna o valor de acordo com a intrução.
funct = {
    'add': 32, 'addu': 33, 'sub': 34, 'subu': 35, 'xor': 38, 'sll': 0, 'srl': 2, 'and': 36,
    'slt': 42, 'or': 37, 'nor': 39, 'mult': 24, 'div': 26, 'mfhi': 16, 'mflo': 18, 'sra': 3,
    'srav': 7, 'sltu': 43, 'jr': 8, 'jalr': 9, 'clo': 33, 'madd': 0, 'msubu': 5, 'mul': 2, 'movn': 11,
    'teq': 52
}
# Dicionário de valores rt dada uma instrução.
rt_code = {
    'bgez': 1, 'bgezal': 17,
}

# Dicionário de instrução tipo .FMT.
functFMT = {
    'add': 0, 'sub': 1, 'mul': 2, 'div': 3
}

# Declaração de dicionários para armazenar labels do .text e as words do .data.
labels = {}
words = {}


def tipo_r(lista_de_parametros, numero_linha):
    """# Função para tratar as instruções tipo R.
# As instruções tipo R tem um padrão na ordem de parametros passados, mas algumas tem suas peculiaridades.
# Essas diferenças são tradatas pelos if statements, de acordo com a insutrção passada.
# Após determinar os valores de cada variável, é chamada uma função para escrever no arquivo de saída."""
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
    elif lista_de_parametros[0] == 'mult' or lista_de_parametros[0] == 'div' or lista_de_parametros[0] == 'teq':
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
    """# Função para tratar as instruções tipo R com semelhanças diferentes da padrão.
# As instruções que são tratadas nessa função possuem semelhanças bem diferentes das padrões do tipo R.
# Função criada para diminuir o uso de if statements e otimizar o código.
# Após determinar os valores de cada variável, é chamada uma função para escrever no arquivo de saída."""
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
    """Tranforma um número negativo em complemento de 2."""
    if imm >= 0:
        return '{:032b}'.format(imm)
    imm = (imm * -1) - 1
    imm = '{:033b}'.format(imm)[1:]
    imm = list(imm)
    for i in range(0, len(imm)):
        imm[i] = '0' if imm[i] == '1' else '1'
    return ''.join(imm)


def branch_target_adress(label):
    """Calcula a distacia do label até o PC+4."""
    global i_text
    bta = labels[label] - (i_text + 1)
    return bta


def converte_string_para_inteiro(n):
    """Converte uma string para um número inteiro."""
    if 'x' in n:
        return int(n, 16)
    return int(n)


def tipo_i(lista_de_parametros, numero_linha):
    """# Função para tratar as instruções tipo I.
    # As instruções tipo I tem um padrão na ordem de parametros passados, mas algumas tem suas peculiaridades.
    # Essas diferenças são tradatas pelos if statements, de acordo com a insutrção passada.
    # Após determinar os valores de cada variável, é chamada uma função para escrever no arquivo de saída."""
    global linha
    # identifica se a instrução usa immediate e separa cria uma lista com a intrução.
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
        if instrucao[0] == 'la':
            rs = registers['zero']
            operacao, rt, word = lista_de_parametros
            imm = words[word]
            rt = registers[rt]
        elif lista_de_parametros[0] == 'lui' or lista_de_parametros[0] == 'li':
            rs = registers['zero']
            operacao, rt, imm = lista_de_parametros
            rt = registers[rt]
            imm = converte_string_para_inteiro(imm)
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

    # transforma o immediate em binário complemento de 2.
    imm_bin = transforma_negativo_em_complemento_de_2(imm)

    imm_mais_significativo, imm_menos_significativo = imm_bin[:16], imm_bin[16:]

    # Tratamento de immediates muito grande.
    # Separação em partes mais significativas para ter a formatação correta na saída.
    if abs(imm) > 65535:
        escrever_output("{:06b}".format(opCode['lui'])
                        + "{:05b}".format(registers['zero'])
                        + "{:05b}".format(registers['at'])
                        + imm_mais_significativo, linha, numero_linha)
        if operacao == 'li' or operacao == 'la':
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
        tipo_r([operacao.replace('i', ''), lista_valores[list(registers.values()).index(rt)],
                lista_valores[list(registers.values()).index(rs)], "at"], numero_linha)
        return
    escrever_output("{:06b}".format(opCode[operacao])
                    + "{:05b}".format(rs)
                    + "{:05b}".format(rt)
                    + imm_menos_significativo, linha, numero_linha)

    return


def tipo_j(lista_de_parametros, numero_linha):
    """# Função para tratar as instruções tipo J."""
    global linha
    operacao = lista_de_parametros[0]
    label = labels[lista_de_parametros[1]]
    escrever_output("{:06b}".format(opCode[operacao])
                    + "{:026b}".format(label), linha, numero_linha)


def tipo_fmt(lista_de_parametros, numero_linha):
    """# Função para tratar as instruções FMT.
    # As instruções tipo FMT trabalham com ponto flutuante de simples ou dupla precisão.
    # Para a otimização de código, foi criada uma função específica, reduzindo o uso de if's."""
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


# Dicionário de tipos de instrução.
# Determina o tipo da instrução passada.
instructionsType = {
    'add': tipo_r, 'addu': tipo_r, 'sub': tipo_r, 'subu': tipo_r, 'xor': tipo_r, 'sll': tipo_r,
    'srl': tipo_r, 'and': tipo_r, 'or': tipo_r, 'nor': tipo_r, 'slt': tipo_r, 'mult': tipo_r,
    'div': tipo_r, 'mfhi': tipo_r, 'mflo': tipo_r, 'sra': tipo_r, 'srav': tipo_r, 'sltu': tipo_r,
    'jr': tipo_r, 'jalr': tipo_r, 'movn': tipo_r, 'teq': tipo_r,

    'clo': tipo_r2, 'madd': tipo_r2, 'msubu': tipo_r2, 'mul': tipo_r2,

    'lw': tipo_i, 'sw': tipo_i, 'beq': tipo_i, 'bne': tipo_i, 'xori': tipo_i, 'lb': tipo_i, 'sb': tipo_i,
    'addi': tipo_i,
    'addiu': tipo_i, 'andi': tipo_i, 'ori': tipo_i, 'lui': tipo_i, 'slti': tipo_i, 'sltiu': tipo_i, 'bgez': tipo_i,
    'bgezal': tipo_i, 'li': tipo_i, 'la': tipo_i,

    'j': tipo_j, 'jal': tipo_j,

    'add.d': tipo_fmt, 'add.s': tipo_fmt, 'sub.d': tipo_fmt, 'sub.s': tipo_fmt,
    'c.eq.d': tipo_fmt, 'c.eq.s': tipo_fmt, 'mul.d': tipo_fmt, 'mul.s': tipo_fmt,
    'div.d': tipo_fmt, 'div.s': tipo_fmt
}


def escrever_output(sla, linha, numero_linha):
    """Função responsável por escrever no arquivo de saída."""
    global i_text
    global nome_arquivo
    if linha != "":
        linha = ("% " + str(numero_linha) + ': ' + linha + " %").replace('\n', '')
    with open(nome_arquivo.replace('.asm', '') + '_text.mif', 'a') as saida_text:
        saida_text.write("{0:08x} : {1:08x};  {2}\n".format(i_text, int(sla, 2), linha))
    i_text += 1


# Verifica se o arquivo de entrada está vazio
if os.stat(nome_arquivo).st_size == 0:
    print("O arquivo de entrada está vazio")
    exit()

# Limpa os arquivos de output para a próxima execução.
# Evitar várias escritas repetidas ao executar o códgio várias vezes.
with open(nome_arquivo.replace('.asm', '') + '_text.mif', 'w') as arquivo_text:
    arquivo_text.write('DEPTH = 4096;\n')
    arquivo_text.write('WIDTH = 32;\n')
    arquivo_text.write('ADDRESS_RADIX = HEX;\n')
    arquivo_text.write('DATA_RADIX = HEX;\n')
    arquivo_text.write('CONTENT\n')
    arquivo_text.write('BEGIN\n')
    arquivo_text.write('\n')
    pass
with open(nome_arquivo.replace('.asm', '') + '_data.mif', 'w') as arquivo_data:
    arquivo_data.write('DEPTH = 16384;\n')
    arquivo_data.write('WIDTH = 32;\n')
    arquivo_data.write('ADDRESS_RADIX = HEX;\n')
    arquivo_data.write('DATA_RADIX = HEX;\n')
    arquivo_data.write('CONTENT\n')
    arquivo_data.write('BEGIN\n')
    arquivo_data.write('\n')
    pass

# Contadores globais.
i_data = 0x10010000
i_text = 0

# Parte onde o arquivo de entrada é aberto.
# Primeiramente as labels são armazenadas para serem usadas no código, independente da sua posição no arquivo de input.
with open(nome_arquivo) as entrada:
    campo = ''
    listaComandos = entrada.readlines()
    # Grava as labels em um dicionário.
    for numero_linha, linha in enumerate(listaComandos):
        numero_linha += 1
        # Formatação da linha do arquivo input.
        linha = linha.replace('$', '').replace(',', ' ').replace('\t', '').replace('\r', '').strip('\n').strip(" ")
        while "  " in linha:
            linha = linha.replace('  ', ' ')
        # Pula linhas em branco.
        if linha == '':
            continue
        # Identifica e salva o campo que o código vai trabalhar, .data ou .text.
        elif linha == '.data' or linha == '.text':
            campo = linha
            continue
        if campo == '.text':
            instrucaoLabel = linha.split(" ")
            i_instru = 0
            if ":" in instrucaoLabel[0]:
                labels[instrucaoLabel[0].replace(':', '')] = int(i_text)
                i_instru += 1
            try:
                if instructionsType[instrucaoLabel[i_instru]].__name__ == 'tipo_i':
                    if len(instrucaoLabel) == i_instru + 3:
                        imm = instrucaoLabel[i_instru + 2]
                    else:
                        imm = instrucaoLabel[i_instru + 3]
                    try:
                        if instrucaoLabel[i_instru] == 'la':
                            i_text += 1
                        else:
                            imm = converte_string_para_inteiro(imm)
                            if abs(imm) > 65535:
                                if instrucaoLabel[i_instru] in ['li']:
                                    i_text += 1
                                else:
                                    i_text += 2
                    except ValueError:
                        pass
            except KeyError:
                pass
            i_text += 1
    i_text = 0
    # Tratamento do arquivo input.
    # É analisado linha por linha e o campo é especificado para que tudo seja tratado da maneira correta.
    for numero_linha, linha in enumerate(listaComandos):
        numero_linha += 1
        # Formatação da linha do arquivo input.
        linha_formatada = linha.replace('$', '').replace(',', ' ').replace('\t', '').replace('\r', '').strip(
            '\n').strip(" ")
        # Remove os espaços duplos.
        while "  " in linha_formatada:
            linha_formatada = linha_formatada.replace('  ', ' ')
        # Pula linhas em branco.
        if linha_formatada == '':
            continue
        # Identifica e salva o campo que o código vai trabalhar, .data ou .text.
        elif linha_formatada == '.data' or linha_formatada == '.text':
            campo = linha_formatada
            continue
        # Tratamento das linhas do campo .data.
        # Salva as words num dicionário identificando o seu nome atrelado ao seu endereço.
        # Escreve as words no arquivo de saída .data.
        if campo == '.data':
            linha_word = linha_formatada.replace(':', '').replace('.word ', '').split(' ')
            words[linha_word.pop(0)] = i_data
            for word in linha_word:
                with open(nome_arquivo.replace('.asm', '') + '_data.mif', 'a') as saida_data:
                    saida_data.write("{0:08x} : {1:08x};\n".format(int((i_data - 0x10010000) / 4),
                                                                   converte_string_para_inteiro(word)))
                i_data += 4
        # Tratamendo das linhas do campo .text.
        # A função do tipo correto da instrução é chamada pela identificação do dicionário dos tipos de instrução.
        # O dicionário retorna o tipo da instrução, chamando a função correta passando os argumentos da entrada.
        elif campo == '.text':
            instrucao = linha_formatada.split(" ")
            if ':' in instrucao[0]:
                instrucao.pop(0)
            # Verifica se a instrução existe
            try:
                instructionsType[instrucao[0]](instrucao, numero_linha)
            except KeyError:
                continue

    # Finaliza os arquivos de saída após passarem por todas as linhas da entrada.
    with open(nome_arquivo.replace('.asm', '') + '_text.mif', 'a') as saida_text:
        saida_text.write('\n')
        saida_text.write('END;\n')
    with open(nome_arquivo.replace('.asm', '') + '_data.mif', 'a') as saida_data:
        saida_data.write('\n')
        saida_data.write('END;\n')

    # Imprime mensagem para notificar que o código foi executado.
    print('Execução concluida')
    print('Arquivos de saída gerados')
