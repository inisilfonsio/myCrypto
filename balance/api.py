"""
Modelo <==> Controlador <==> Vista

Modelo <////////> Vista  NUNCA hay comunicación entre Modelo y Vista

La vista interactúa con el usuario:
1. entrada de datos
2. muestra datos
TODO: Clase CriptoView
"""


class CriptoView:

    def pedir_monedas(self):
        origen = input('¿Qué moneda quieres cambiar? ')
        origen = origen.upper()
        destino = input('¿Qué moneda deseas obtener? ')
        destino = destino.upper()

        return (origen, destino)

    def mostrar_cambio(self, origen, destino, cambio):
        print(f'Un {origen} vale lo mismo que {cambio:,.2f} {destino}')

    def quieres_seguir(self):
        seguir = input('¿Quieres consultar de nuevo? (S/N) ')
        return seguir
