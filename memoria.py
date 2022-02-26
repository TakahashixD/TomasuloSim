class Memoria:
    def __init__(self):
        self.memoria = []
        for i in range(0, 512):
            self.memoria.append(i*0)
#carrega da memoria    
    def carregar(self, endereco):
        return self.memoria[int(endereco)]

#armazena na memoria
    def armazenar(self, endereco, valor):
        self.memoria[int(endereco)] = valor

    def get_memoria(self):
        return self.memoria