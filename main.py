import tomasulo
import instrucoes


def read_input(input):
    file = open(input)
    input = file.read().splitlines()

    instructions = []
    for line in input:
        instructions.append(line)
    return instructions

def main():
    #trocar o arquivo do "read_input" caso queira testas outro arquivo txt
    input_list = read_input('teste1.txt')
    inst = []
    valores = []
    for item in input_list:
        itens = item.split(' ')
        inst.append(itens[0])
        valores.append(itens[1])
    param = []
    for i in valores:
        troca1 = i.replace('(', ',')
        troca2 = troca1.replace(')', '')
        j = troca2.split(',')
        param.append(j)
    k = 0
    instr = []
    while k != len(input_list):
        if inst[k] == 'j':
            instr.append(instrucoes.criar_jump_incod(inst[k], param[k][0]))
        elif inst[k] in ['subi', 'addi', 'blt', 'bgt', 'beq', 'bne']:
            instr.append(instrucoes.criar_instrucao_imediata(inst[k], param[k][0], param[k][1], param[k][2]))
        elif inst[k] in ['sw', 'lw']:
            instr.append(instrucoes.criar_instrucao_imediata(inst[k], param[k][0], param[k][2], param[k][1]))
        else:
            instr.append(instrucoes.criar_instrucao(inst[k], param[k][0], param[k][1], param[k][2]))
        k += 1
    
    conjunto_inst = instrucoes.Conjunto_instrucoes(instr)
    tomasulo_imp = tomasulo.Tomasulo(conjunto_inst)
    tomasulo_imp.atualizar()

main()
