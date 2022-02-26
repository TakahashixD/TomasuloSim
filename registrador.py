class Registrador:
    def __init__(self, valor, status):
        self.valor = int(valor)
        self.status = status

class Status_Registrador:
    def __init__(self):
        self.reg = {}
        for i in range(0,32):
            self.reg['r' + str(i)] = Registrador(0, True)



    def print_status(self):
        for i in range(0,32):
            print('r' + str(i) + ": " + str(self.reg['r' + str(i)].valor), end=" ")

#retorna o status do registrador
    def pronto(self, reg):
        return self.reg[reg].status

#retorna o status de todos registradores
    def get_status(self):
        status = []
        for i in range(0,32):            
            status.append(self.reg['r' + str(i)].valor)
        return status

#retorna o valor do registrador
    def get_valor(self, reg):
        return self.reg[reg].valor

#seta o valor e o status de um registrador
    def set_valor_e_status(self, reg, valor, status):
        self.reg[reg].valor = valor
        self.reg[reg].status = status