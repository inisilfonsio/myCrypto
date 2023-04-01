from .models import CriptoModel
from .api import CriptoView


class CriptoController:

    def __init__(self):
        self.modelo = CriptoModel()
        self.vista = CriptoView()

    def consultar(self):
        seguir = 's'
        while seguir.lower() == 's':
            ori, des = self.vista.pedir_monedas()

            self.modelo.origen = ori
            self.modelo.destino = des
            self.modelo.consultar_cambio()

            self.vista.mostrar_cambio(ori, des, self.modelo.cambio)

            seguir = ''
            while seguir.lower() not in ('s', 'n'):
                seguir = self.vista.quieres_seguir()
