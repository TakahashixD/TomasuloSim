
class Instrucao:
	def __init__(self, op):
		self.status = 'esperando'
		self.nome = ''
		self.tipo = ''
		self.unidade = ''
		self.ciclos_executados = 0
		self.ciclos_total = 0
		self.op = op

		if op in ['add', 'addi', 'sub', 'subi', 'and', 'or', 'not', 'blt', 'bgt', 'beq', 'bne', 'j']:
			self.tipo_unidade = 'Add'
		elif op in ['lw', 'sw']:
			self.tipo_unidade = 'Mem'
		elif op in ['mul', 'div']:
			self.tipo_unidade = 'Mul'
		else:
			raise Exception("Unidade desconhecida: " + op)

	def emissao(self, unidade):
		self.status = 'emissao'
		self.unidade = unidade

	def executar(self):
		if self.status == 'emissao':
			self.ciclos_executados = self.ciclos_total
		# print('\nExec ' + self.nome + ': ' + str(self.ciclos_executados))
		self.status = 'exec'
		self.ciclos_executados -= 1

	def escrever(self):
		self.status = 'escrita'
	
	def finalizar(self):
		self.status = 'finalizado'
		
	def get_status(self):
		return self.status

	def get_tipo(self):
		return self.tipo

	def deve_escrever(self):
		return self.op in ['add', 'addi', 'sub', 'subi', 'lw', 'mul', 'div']

	def pronto_para_exec(self):
		return self.unidade.Vj != '' and self.unidade.Vk != ''
		
	def print_status(self):
		print("%20s" %self.nome + ' ' + "%6s" %str(self.status == 'emissao') + ' ' + "%6s" %str(self.status == 'exec') + ' ' + "%6s" %str(self.status == 'escrita'))


class criar_instrucao(Instrucao):
	def __init__(self, op, rd, rs, rt):
		Instrucao.__init__(self, op)
		self.tipo = '1'
		self.op = op
		self.rs = rs
		self.rt = rt
		self.rd = rd
		self.nome = op + ' ' + rd + ',' + rs + ',' + rt

		if op == 'mul':
			self.ciclos_executados = 15
		elif op == 'div':
			self.ciclos_executados = 25
		else:
			self.ciclos_executados = 5

		self.ciclos_total = self.ciclos_executados

class criar_instrucao_imediata(Instrucao):
	def __init__(self, op, rs, rt, imediato):
		Instrucao.__init__(self, op)
		self.tipo = '2'
		self.op = op
		self.rs = rs
		self.rt = rt
		self.imediato = int(imediato)

		if op == 'lw' or op == 'sw':
			self.ciclos_executados = 5
			self.nome = op + ' ' + rs + ',' + imediato + '(' + rt + ')'
		else:
			self.ciclos_executados = 5
			if op in ['subi', 'addi', 'blt', 'bgt', 'beq', 'bne']:
				self.nome = op + ' ' + rs + ',' + rt + ',' + imediato

		self.ciclos_total = self.ciclos_executados

class criar_jump_incod(Instrucao):
	def __init__(self, op, endereco):
		Instrucao.__init__(self, op)
		self.tipo = '3'
		self.op = op
		self.ciclos_total = 5
		self. endereco =  endereco
		self.nome = op + ' ' +  endereco
		self.ciclos_executados = self.ciclos_total

class Conjunto_instrucoes:
    def __init__(self, instrucoes):
        self.todas = instrucoes
        self.PC = 0

    def get_prox(self):
        return self.todas[self.PC]

    def atualizar_PC(self, count=1):
        self.PC += int(count)

    def set_PC(self, i):
        self.PC = int(i)

    def print_status(self):
        for i in self.todas:
            i.print_status()

    def terminou(self):
        return self.PC >= len(self.todas)

    # def get_status(self):
    #     status = []
    #     for i in self.todas:
    #         status.append(i.get_status())
    #     return [self.PC, status]