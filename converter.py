import dicionarios

def tipoR(instrucao):
    operacao, rd, rs, rt = instrucao
    return ("{:06b}".format(dicionarios.opCode[operacao]) +
            "{:05b}".format(dicionarios.registers[rs[1:3]]) +
            "{:05b}".format(dicionarios.registers[rt[1:3]]) +
            "{:05b}".format(dicionarios.registers[rd[1:3]]) +
            "{:05b}".format(dicionarios.chamt[operacao]) +
            "{:06b}".format(dicionarios.funct[operacao]))


with open('input.txt') as entrada:
    codigo = entrada.readlines()
    for i in range(0, len(codigo)):
        linha = codigo[i]
        instrucao = linha.split(" ")
        print(tipoR(instrucao))
        print("{0:08x} : {1:08} ; % {2} %".format(i, hex(int(tipoR(instrucao), 2)), linha[:-1]))
