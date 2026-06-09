from GestorEntidad import GestorEntidad
from abc import abstractmethod
from datetime import datetime
import re

class PersonaBase(GestorEntidad):

    def __init__(self):
        self.nombre = ""
        self.apellidos = ""
        self.fecha_nacimiento = ""

    @abstractmethod
    def ingresar_datos(self):
        self.nombre = input("Nombre: ").strip()
        while not self.nombre:
            print("Error: el nombre no puede estar vacío.")
            self.nombre = input("Nombre: ").strip()

        self.apellidos = input("Apellidos: ").strip()
        while not self.apellidos:
            print("Error: los apellidos no pueden estar vacíos.")
            self.apellidos = input("Apellidos: ").strip()

        while True:
            fecha_str = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
            if not fecha_str:
                print("Error: la fecha de nacimiento no puede estar vacía.")
                continue
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                if fecha > datetime.now():
                    print("Error: la fecha de nacimiento no puede ser en el futuro.")
                    continue
                self.fecha_nacimiento = fecha_str
                break
            except ValueError:
                print("Error: formato de fecha inválido. Usa YYYY-MM-DD (ej: 1990-05-15).")

    @abstractmethod
    def obtener_datos(self):
        return f"{self.nombre}, {self.apellidos}, {self.fecha_nacimiento}"
