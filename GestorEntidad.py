from abc import ABC, abstractmethod

class GestorEntidad(ABC):

    @abstractmethod
    def registrar(self, dato):
        pass

    @abstractmethod
    def actualizar(self, indice, nuevo_dato):
        pass

    @abstractmethod
    def consultar(self):
        pass

    @abstractmethod
    def eliminar(self, indice):
        pass
