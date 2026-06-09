from GestorEntidad import GestorEntidad
from abc import abstractmethod

class OperacionRegistro(GestorEntidad):

    def __init__(self):
        self.id = 0

    @abstractmethod
    def ingresar_datos(self):
        pass

    @abstractmethod
    def obtener_datos(self):
        pass

    @abstractmethod
    def procesar(self):
        pass
