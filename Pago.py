from OperacionRegistro import OperacionRegistro
from conexion import obtener_conexion
from datetime import datetime

class Pago(OperacionRegistro):

    def __init__(self):
        super().__init__()
        self.fecha_pago = ""
        self.monto_pagado = 0.0
        self.metodo_pago = ""
        self.referencia = ""
        self.poliza_id = 0

    def ingresar_datos(self):
        while True:
            fecha_str = input("Fecha del pago (DD/MM/YYYY): ").strip()
            if not fecha_str:
                print("Error: la fecha del pago no puede estar vacía.")
                continue
            try:
                self.fecha_pago = datetime.strptime(fecha_str, "%d/%m/%Y")
                break
            except ValueError:
                print("Error: formato de fecha inválido. Usa DD/MM/YYYY (ej: 15/05/2024).")

        while True:
            try:
                valor = input("Monto pagado: ").strip()
                if not valor:
                    print("Error: el monto no puede estar vacío.")
                    continue
                self.monto_pagado = float(valor)
                if self.monto_pagado <= 0:
                    print("Error: el monto debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número válido (ej: 1500.00).")

        self.metodo_pago = input("Método de pago: ").strip()
        while not self.metodo_pago:
            print("Error: el método de pago no puede estar vacío.")
            self.metodo_pago = input("Método de pago: ").strip()

        self.referencia = input("Referencia: ").strip()
        while not self.referencia:
            print("Error: la referencia no puede estar vacía.")
            self.referencia = input("Referencia: ").strip()

        while True:
            try:
                valor = input("ID de póliza: ").strip()
                if not valor:
                    print("Error: el ID de póliza no puede estar vacío.")
                    continue
                self.poliza_id = int(valor)
                if self.poliza_id <= 0:
                    print("Error: el ID de póliza debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número entero válido.")

    def obtener_datos(self):
        return (f"{self.fecha_pago.strftime('%Y-%m-%d')}, {self.monto_pagado}, "
                f"{self.metodo_pago}, {self.referencia}, {self.poliza_id}")

    def procesar(self):
        if self.monto_pagado <= 0:
            print("Error: el monto debe ser mayor a 0.")
            return False
        if self.poliza_id <= 0:
            print("Error: la póliza no es válida.")
            return False
        print("Pago procesado correctamente.")
        return True

    def registrar(self, dato=None):
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO pagos
                     (fecha_pago, monto_pagado, metodo_pago, referencia, poliza_id)
                     VALUES (%s, %s, %s, %s, %s)"""
            valores = (self.fecha_pago.strftime('%Y-%m-%d'),
                       self.monto_pagado, self.metodo_pago,
                       self.referencia, self.poliza_id)
            cursor.execute(sql, valores)
            conn.commit()
            self.id = cursor.lastrowid
            print(f"Pago registrado con ID: {self.id}")
        except Exception as e:
            print(f"Error al registrar pago: {e}")
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
            sql = """UPDATE pagos SET
                     fecha_pago=%s, monto_pagado=%s, metodo_pago=%s,
                     referencia=%s, poliza_id=%s
                     WHERE id_pago=%s"""
            valores = (self.fecha_pago.strftime('%Y-%m-%d'),
                       self.monto_pagado, self.metodo_pago,
                       self.referencia, self.poliza_id, indice)
            cursor.execute(sql, valores)
            conn.commit()
            print("Pago actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar pago: {e}")
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
            cursor.execute("SELECT * FROM pagos")
            filas = cursor.fetchall()
            if not filas:
                print("No hay pagos registrados.")
            for fila in filas:
                print(fila)
        except Exception as e:
            print(f"Error al consultar pagos: {e}")
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
            cursor.execute("DELETE FROM pagos WHERE id_pago=%s", (indice,))
            conn.commit()
            print(f"Pago con ID {indice} eliminado.")
        except Exception as e:
            print(f"Error al eliminar pago: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
