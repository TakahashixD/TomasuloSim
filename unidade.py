class Unidade:
    def __init__(self, nome):
        self.nome = nome
        self.Busy = False
        self.Op = ''
        self.Vj = ''
        self.Vk = ''
        self.Qj = ''
        self.Qk = ''
        self.A = ''
    #dado  gerado  por  uma  instrução antecipa envio para outra que a requisita.
    def bypass(self, dependencia, resultado):
        if self.nome != dependencia:
            if self.Qj == dependencia:
                self.Qj = ''
                self.Vj = resultado
            
            if self.Qk == dependencia:
                self.Qk = ''
                self.Vk = resultado

    def print_status(self):
        print("%7s: " %self.nome + "%6s" %self.Busy + ' ' + "%20s" %self.Op + ' ' + "%6s" %self.Vj + ' ' + "%6s" %self.Vk + ' ' + "%6s" %self.Qj + ' ' + "%6s" %self.Qk + ' ' + "%6s" %self.A)

