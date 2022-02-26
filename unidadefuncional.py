from unidade import Unidade
#cria unidades funcionais
class Unidades_Funcionais:
    def __init__(self):
        self.load0 = Unidade("load0")
        self.load1 = Unidade("load1")
        self.load2 = Unidade("load2")
        self.add0 = Unidade("add0")
        self.add1 = Unidade("add1")
        self.add2 = Unidade("add2")
        self.mult0 = Unidade("mult0")
        self.mult1 = Unidade("mult1")
        self.mult2 = Unidade("mult2")

#retorna o status da unidade
    def status_unidade(self, tipo):
        if tipo == 'Add':
            return self.add_disponivel()
        elif tipo == 'Mem':
            return self.load_disponivel()
        elif tipo == 'Mul':
            return self.mul_diponivel()

#retorna a unidades não ocupadas (Busy)
    def get_unidade_exec(self, tipo):
        if(self.status_unidade(tipo)):
            if tipo == 'Add':
                if not self.add0.Busy:
                    return self.add0
                elif not self.add1.Busy:
                    return self.add1
                elif not self.add2.Busy:
                    return self.add2
            elif tipo == 'Mem':
                if not self.load0.Busy:
                    return self.load0
                elif not self.load1.Busy:
                    return self.load1
                elif not self.load2.Busy:
                    return self.load2
            elif tipo == 'Mul':                
                if not self.mult0.Busy:
                    return self.mult0
                elif not self.mult1.Busy:
                    return self.mult1
                elif not self.mult2.Busy:
                    return self.mult2
        else:
            raise Exception("Unidade não disponivel: " + tipo)

#retorna a unidade disponivel de cada tipo
    def load_disponivel(self):
        return ((not self.load0.Busy) or (not self.load1.Busy) or (not self.load2.Busy))

    def add_disponivel(self):
        return ((not self.add0.Busy) or (not self.add1.Busy) or (not self.add2.Busy))

    def mul_diponivel(self):
        return ((not self.mult0.Busy) or (not self.mult1.Busy) or (not self.mult2.Busy))

#retorna o status de cada unidade
    def get_status(self):
        return [
                self.load0.get_status(), 
                self.load1.get_status(),
                self.load2.get_status(),
                self.add0.get_status(),
                self.add1.get_status(),
                self.add2.get_status(),
                self.mult0.get_status(),
                self.mult1.get_status(),
                self.mult2.get_status()
                ]
#printa como está cada unidade
    def print_status(self):
        self.load0.print_status()
        self.load1.print_status()
        self.load2.print_status()
        self.add0.print_status()
        self.add1.print_status()
        self.add2.print_status()
        self.mult0.print_status()
        self.mult1.print_status()
        self.mult2.print_status()

    def bypass(self, dependencia, resultado):
        self.load0.bypass(dependencia, resultado)
        self.load1.bypass(dependencia, resultado)
        self.add0.bypass(dependencia, resultado)
        self.add1.bypass(dependencia, resultado)
        self.add2.bypass(dependencia, resultado)
        self.mult0.bypass(dependencia, resultado)
        self.mult1.bypass(dependencia, resultado)