import memoria
import registrador
import unidadefuncional
import instrucoes

class Tomasulo:
    def __init__(self, conjunto_instrucoes):
        self.conjunto_instrucoes = conjunto_instrucoes
        self.unidades = unidadefuncional.Unidades_Funcionais()
        self.registradores = registrador.Status_Registrador()
        self.memoria = memoria.Memoria()
        self.ciclos = 0
        self.instrucao_emitida = 0
        self.add_pronto = True
        self.mult_pronto = True
        self.mem_pronto = True
        #The Common Data Bus (CDB) connects reservation stations directly to 
        # functional units. According to Tomasulo it "preserves precedence while encouraging concurrency".
        self.barramentos_pronto = True
        #espera em operações de desvio
        self.esperando_desvio = False

    def atualizar(self):
        self.show_status()
        while not self.terminado():
            self.ciclos += 1
            self.finalizar()
            self.escrever()
            self.executar()
            self.emissao()
            self.show_status()

    # Pega a próxima instrução e a emite, dependendo qual unidade estiver disponivel
    def emissao(self):
        #se o conjuto de instrucoes nao terminou e nao estiver esperando o branch
        if not self.conjunto_instrucoes.terminou() and not self.esperando_desvio:
            #pega a proxima instrucao
            i = self.conjunto_instrucoes.get_prox()
            # ve se existe alguma unidade funcional disponivel
            if self.unidades.status_unidade(i.tipo_unidade):
                #incrementa o count do cojunto de instrucoes. PC = PC + 1.
                self.conjunto_instrucoes.atualizar_PC()
                self.instrucao_emitida += 1
                #pega uma unidade disponivel
                unidade = self.unidades.get_unidade_exec(i.tipo_unidade)
                # recebe o status de 'emissao'
                i.emissao(unidade)
                unidade.Busy = True
                unidade.Op = i.nome  
                #atribui Vj e Vk. Se existirem depencias utiliza Qj e Qk
                self.config_exec(i)
                #caso for um operacao de branch
                if i.op in ['blt', 'bgt', 'beq', 'bne']:
                    self.esperando_desvio = True

    # pega todas as instruções emitidas e as executa
    def executar(self):
        for i in self.conjunto_instrucoes.todas:
            if i.get_status() == 'emissao':
                #dependecias terminaram sua exec (Vj e VK diferente de "vazio")
                if i.pronto_para_exec():
                    if i.tipo_unidade == 'Add' and self.add_pronto:
                        self.add_pronto = False
                        i.executar()
                    if i.tipo_unidade == 'Mul' and self.mult_pronto:
                        self.mult_pronto = False
                        i.executar()
                    if i.tipo_unidade == 'Mem' and self.mem_pronto:
                        self.mem_pronto = False
                        i.executar()
            elif i.get_status() == 'exec':
                i.executar()

    def tipo1(self, i):
        if i.op == 'add':
            resultado = i.unidade.Vj + i.unidade.Vk
        elif i.op == 'sub':
            resultado = i.unidade.Vj - i.unidade.Vk
        elif i.op == 'mul':
            resultado = i.unidade.Vj * i.unidade.Vk
        elif i.op == 'div':
            resultado = i.unidade.Vj / i.unidade.Vk
        elif i.op == 'and':
            resultado = i.unidade.Vj and i.unidade.Vk
        elif i.op == 'or':
            resultado = i.unidade.Vj or i.unidade.Vk
        elif i.op == 'not':
            resultado = not i.unidade.Vj
        #escreve apenas se rd está esperando por essa op
        if i.unidade.nome == self.registradores.get_valor(i.rd):
            self.registradores.set_valor_e_status(i.rd, resultado, True) 
        #bypass o resultado
        self.unidades.bypass(i.unidade.nome, resultado)
        i.unidade.A = resultado

    def tipo2(self, i):
        if i.op == 'blt':
            self.esperando_desvio = False
            if i.unidade.Vj < i.unidade.Vk:
                self.conjunto_instrucoes.set_PC(i.imediato)
        elif i.op == 'bgt':
            self.esperando_desvio = False
            if i.unidade.Vj > i.unidade.Vk:
                self.conjunto_instrucoes.set_PC(i.imediato)
        elif i.op == 'beq':
            self.esperando_desvio = False
            if i.unidade.Vj == i.unidade.Vk:
                self.conjunto_instrucoes.atualizar_PC(1 + i.imediato)
        elif i.op == 'bne':
            self.esperando_desvio = False
            if i.unidade.Vj != i.unidade.Vk:
                self.conjunto_instrucoes.atualizar_PC(1 + i.imediato)
        elif i.op == 'sw':
            self.memoria.armazenar(i.imediato + i.unidade.Vk, i.unidade.Vj)
        #subi, addi, lw precisam passar pelo bypass
        elif i.op in ['subi', 'addi', 'lw']:
            if i.op == 'lw':
                resultado = self.memoria.carregar(i.unidade.Vj + i.unidade.Vk)
            elif i.op == 'addi':
                resultado = i.unidade.Vj + i.unidade.Vk
            elif i.op == 'subi':
                resultado = i.unidade.Vj - i.unidade.Vk
            #escreve apenas se rd está esperando por essa op
            if i.unidade.nome == self.registradores.get_valor(i.rs): 
                self.registradores.set_valor_e_status(i.rs, resultado, True) 
            #bypass o resultado
            self.unidades.bypass(i.unidade.nome, resultado)
            i.unidade.A = resultado

    # pega todas instruções de execução, se terminaram de executar escreve-as
    def escrever(self):
        for i in self.conjunto_instrucoes.todas:
            if i.get_status() == 'exec' and i.ciclos_executados <= 0:
                #caso barra estiver livre ou i nao esta entre add, addi, sub, subi, mul, div e lw(ops que não escrevem)
                if self.barramentos_pronto or (not i.deve_escrever()):
                    i.escrever()
                    #caso a op deve escrever
                    if i.deve_escrever():
                        #ocupa o barramento
                        self.barramentos_pronto = False  
                    #para qual unidade a instrucao sera alocada
                    if i.tipo_unidade == 'Add':
                        self.add_pronto = True
                    elif i.tipo_unidade == 'Mul':
                        self.mult_pronto = True
                    elif i.tipo_unidade == 'Mem':
                        self.mem_pronto = True
                #qual o tipo da instrucao normal(1) ou imediata(2) ou um jump incondicional(3)
                if i.tipo == '1':
                    self.tipo1(i)
                elif i.tipo == '2':
                    self.tipo2(i)
                elif i.tipo == '3':
                    self.conjunto_instrucoes.set_PC(i.endereco)

    def finalizar(self):
        for i in self.conjunto_instrucoes.todas:
            if i.get_status() == 'escrita':
                if i.deve_escrever():
                    self.barramentos_pronto = True
                i.unidade.Busy = False
                i.unidade.Op = ''
                i.unidade.Vj = ''
                i.unidade.Vk = ''
                i.unidade.Qj = ''
                i.unidade.Qk = ''
                i.unidade.A = '' 
                i.finalizar()

#
    def config_exec(self, i):
        if i.op == 'j':
            i.unidade.Vj = ''
            i.unidade.Vk = ''
        else:
            if self.registradores.pronto(i.rs):
                i.unidade.Vj = self.registradores.get_valor(i.rs)  # coloca o valor dos registradores em Vj
            else:
                i.unidade.Qj = self.registradores.get_valor(i.rs)  # esperando dependencia

            if i.op not in ['subi', 'addi', 'lw']:  # add,sub, mul, div, blt, bgt, beq, bne e sw utilizam rt
                if self.registradores.pronto(i.rt):
                    i.unidade.Vk = self.registradores.get_valor(i.rt)  # coloca o valor dos registradores em Vk
                else:
                    i.unidade.Qk = self.registradores.get_valor(i.rt)  # esperando dependencia
            else:
                i.unidade.Vk = i.imediato

            if i.tipo == '1':
                self.registradores.set_valor_e_status(i.rd, i.unidade.nome, False)
            elif i.tipo == '2':
                if  i.op in ['subi', 'addi', 'lw']:
                    self.registradores.set_valor_e_status(i.rs, i.unidade.nome, False)

    def show_status(self):
        print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        print('\nCiclos: ' + str(self.ciclos))

        print('\nConjunto de instruções')
        print("         Op           Emis    Exec   Escr  ")
        self.conjunto_instrucoes.print_status()

        print('\nUnidades funcionais')
        print(
            "   Stat    Busy           Op            Vj     Vk     Qj     Qk     A   ")
        self.unidades.print_status()

        print('\nRegistradores')
        self.registradores.print_status()
        print()
        print('\nMemoria')
        print(self.memoria.get_memoria())

    def terminado(self):
        return all(i.get_status() == 'finalizado' for i in self.conjunto_instrucoes.todas)
