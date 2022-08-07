import dicionarios


def tipoR(linha):
    instrucao = linha.strip('\n').split(" ")
    operacao, rd, rs, rt = instrucao
    return ("{:06b}".format(dicionarios.opCode[operacao]) +
            "{:05b}".format(dicionarios.registers[rs[1:3]]) +
            "{:05b}".format(dicionarios.registers[rt[1:3]]) +
            "{:05b}".format(dicionarios.registers[rd[1:3]]) +
            "{:05b}".format(dicionarios.chamt[operacao]) +
            "{:06b}".format(dicionarios.funct[operacao]))


def tipoI(linha):
    instrucao = linha.strip('\n').split(" ")
    if (linha.count(",") == 2):
        operacao, rt, rs, imm = instrucao
        binario = ("{:06b}".format(dicionarios.opCode[operacao]) +
                   "{:05b}".format(dicionarios.registers[rs[1:3]]) +
                   "{:05b}".format(dicionarios.registers[rt[1:3]]) +
                   "{:016b}".format(int(imm)))
        return binario
    operacao, rt, imm_rs = instrucao
    imm, rs = imm_rs[:-1].split("(")
    binario = ("{:06b}".format(dicionarios.opCode[operacao]) +
               "{:05b}".format(dicionarios.registers[rs[1:]]) +
               "{:05b}".format(dicionarios.registers[rt[1:3]]) +
               "{:016b}".format(int(imm)))
    return binario


with open('input.txt') as entrada:
    codigo = entrada.readlines()
    for i in range(0, 2):
        linha = codigo[i]
        print("{0:08x} : {1:08x} ; % {2} %".format(i, int(tipoR(linha), 2), linha[:-1].strip('\n')))
    for i in range(2, len(codigo)):
        linha = codigo[i]
        print("{0:08x} : {1:08x} ; % {2} %".format(i, int(tipoI(linha), 2), linha.strip('\n')))
