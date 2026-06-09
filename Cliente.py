from PersonaBase import PersonaBase
from conexion import obtener_conexion
import re

class Cliente(PersonaBase):

    def __init__(self):
        super().__init__()
        self.id_cliente = 0
        self.genero = ""
        self.curp = ""
        self.telefono = ""
        self.correo = ""
        self.ocupacion = ""
        self.ingreso_mensual = 0.0

    def ingresar_datos(self):
        super().ingresar_datos()

        opciones_genero = ["masculino", "femenino", "otro"]
        self.genero = input("Género (Masculino/Femenino/Otro): ").strip()
        while self.genero.lower() not in opciones_genero:
            print(f"Error: género inválido. Opciones: {', '.join(opciones_genero)}")
            self.genero = input("Género (Masculino/Femenino/Otro): ").strip()

        self.curp = input("CURP: ").strip().upper()
        while len(self.curp) != 18:
            print(f"Error: la CURP debe tener exactamente 18 caracteres (ingresaste {len(self.curp)}).")
            self.curp = input("CURP: ").strip().upper()

        self.telefono = input("Teléfono (10 dígitos): ").strip()
        while len(self.telefono) != 10 or not self.telefono.isdigit():
            if not self.telefono.isdigit():
                print("Error: el teléfono solo debe contener dígitos (0-9).")
            else:
                print(f"Error: el teléfono debe tener 10 dígitos (ingresaste {len(self.telefono)}).")
            self.telefono = input("Teléfono (10 dígitos): ").strip()

        self.correo = input("Correo electrónico: ").strip()
        while not self._validar_correo(self.correo):
            self.correo = input("Correo electrónico: ").strip()

        self.ocupacion = input("Ocupación: ").strip()
        while not self.ocupacion:
            print("Error: la ocupación no puede estar vacía.")
            self.ocupacion = input("Ocupación: ").strip()

        while True:
            try:
                valor = input("Ingreso mensual: ").strip()
                if not valor:
                    print("Error: el ingreso mensual no puede estar vacío.")
                    continue
                self.ingreso_mensual = float(valor)
                if self.ingreso_mensual < 0:
                    print("Error: el ingreso mensual no puede ser negativo.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número válido (ej: 15000.50).")

    def _validar_correo(self, correo):
        if not correo:
            print("Error: el correo no puede estar vacío.")
            return False
        if "@" not in correo:
            print("Error: el correo debe contener '@' (ej: usuario@dominio.com).")
            return False
        partes = correo.split("@")
        if len(partes) != 2:
            print("Error: el correo solo debe tener un '@'.")
            return False
        usuario, dominio = partes
        if not usuario:
            print("Error: falta el nombre de usuario antes del '@'.")
            return False
        if not dominio or "." not in dominio:
            print("Error: el dominio del correo es inválido (ej: gmail.com, hotmail.com).")
            return False
        partes_dominio = dominio.split(".")
        if any(not parte for parte in partes_dominio):
            print("Error: el dominio del correo tiene un formato inválido.")
            return False
        return True

    def obtener_datos(self):
        return super().obtener_datos() + \
               f", {self.genero}, {self.curp}, {self.telefono}, {self.correo}, {self.ocupacion}, {self.ingreso_mensual}"

    def registrar(self, dato=None):
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO clientes 
                     (nombre, apellidos, fecha_nacimiento, genero, curp, telefono, correo, ocupacion, ingreso_mensual)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (self.nombre, self.apellidos, self.fecha_nacimiento,
                       self.genero, self.curp, self.telefono,
                       self.correo, self.ocupacion, self.ingreso_mensual)
            cursor.execute(sql, valores)
            conn.commit()
            self.id_cliente = cursor.lastrowid
            print(f"Cliente registrado con ID: {self.id_cliente}")
        except Exception as e:
            print(f"Error al registrar cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def actualizar(self, indice, nuevo_dato=None):
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """UPDATE clientes SET
                     nombre=%s, apellidos=%s, fecha_nacimiento=%s,
                     genero=%s, curp=%s, telefono=%s,
                     correo=%s, ocupacion=%s, ingreso_mensual=%s
                     WHERE id_cliente=%s"""
            valores = (self.nombre, self.apellidos, self.fecha_nacimiento,
                       self.genero, self.curp, self.telefono,
                       self.correo, self.ocupacion, self.ingreso_mensual, indice)
            cursor.execute(sql, valores)
            conn.commit()
            print("Cliente actualizado correctamente")
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def consultar(self):
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            filas = cursor.fetchall()
            if not filas:
                print("No hay clientes registrados.")
            for fila in filas:
                print(fila)
        except Exception as e:
            print(f"Error al consultar clientes: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def eliminar(self, indice):
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (indice,))
            conn.commit()
            print(f"Cliente con ID {indice} eliminado")
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
