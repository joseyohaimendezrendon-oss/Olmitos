from GestorEntidad import GestorEntidad
from conexion import obtener_conexion
from datetime import datetime

class Poliza(GestorEntidad):

    def __init__(self):
        self.id_poliza = 0
        self.numero_poliza = 0
        self.fecha_inicio = ""
        self.fecha_fin = ""
        self.prima_mensual = 0.0
        self.suma_asegurada = 0.0
        self.tipo_poliza = ""
        self.estatus = ""
        self.cliente_id = 0

    def ingresar_datos(self):
        while True:
            try:
                valor = input("Número de póliza: ").strip()
                if not valor:
                    print("Error: el número de póliza no puede estar vacío.")
                    continue
                self.numero_poliza = int(valor)
                if self.numero_poliza <= 0:
                    print("Error: el número de póliza debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número entero válido.")

        while True:
            fecha_str = input("Fecha inicio (DD/MM/YYYY): ").strip()
            if not fecha_str:
                print("Error: la fecha de inicio no puede estar vacía.")
                continue
            try:
                self.fecha_inicio = datetime.strptime(fecha_str, "%d/%m/%Y")
                break
            except ValueError:
                print("Error: formato de fecha inválido. Usa DD/MM/YYYY (ej: 15/05/2024).")

        while True:
            fecha_str = input("Fecha fin (DD/MM/YYYY): ").strip()
            if not fecha_str:
                print("Error: la fecha de fin no puede estar vacía.")
                continue
            try:
                self.fecha_fin = datetime.strptime(fecha_str, "%d/%m/%Y")
                if self.fecha_inicio >= self.fecha_fin:
                    print("Error: la fecha de fin debe ser posterior a la fecha de inicio.")
                    continue
                break
            except ValueError:
                print("Error: formato de fecha inválido. Usa DD/MM/YYYY (ej: 15/05/2025).")

        while True:
            try:
                valor = input("Prima mensual: ").strip()
                if not valor:
                    print("Error: la prima mensual no puede estar vacía.")
                    continue
                self.prima_mensual = float(valor)
                if self.prima_mensual <= 0:
                    print("Error: la prima debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número válido (ej: 1500.00).")

        while True:
            try:
                valor = input("Suma asegurada: ").strip()
                if not valor:
                    print("Error: la suma asegurada no puede estar vacía.")
                    continue
                self.suma_asegurada = float(valor)
                if self.suma_asegurada <= 0:
                    print("Error: la suma asegurada debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número válido (ej: 500000.00).")

        self.tipo_poliza = input("Tipo de póliza: ").strip()
        while not self.tipo_poliza:
            print("Error: el tipo de póliza no puede estar vacío.")
            self.tipo_poliza = input("Tipo de póliza: ").strip()

        opciones_estatus = ["vigente", "vencida", "cancelada"]
        self.estatus = input("Estatus (vigente/vencida/cancelada): ").strip()
        while self.estatus.lower() not in opciones_estatus:
            print(f"Error: estatus inválido. Opciones: {', '.join(opciones_estatus)}")
            self.estatus = input("Estatus (vigente/vencida/cancelada): ").strip()

        while True:
            try:
                valor = input("ID del cliente: ").strip()
                if not valor:
                    print("Error: el ID del cliente no puede estar vacío.")
                    continue
                self.cliente_id = int(valor)
                if self.cliente_id <= 0:
                    print("Error: el ID del cliente debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número entero válido.")

    def obtener_datos(self):
        return (f"{self.numero_poliza}, {self.fecha_inicio.strftime('%Y-%m-%d')}, "
                f"{self.fecha_fin.strftime('%Y-%m-%d')}, {self.prima_mensual}, "
                f"{self.suma_asegurada}, {self.tipo_poliza}, {self.estatus}, {self.cliente_id}")

    def registrar(self, dato=None):
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO polizas
                     (numero_poliza, fecha_inicio, fecha_fin, prima_mensual,
                      suma_asegurada, tipo_poliza, estatus, cliente_id)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (self.numero_poliza,
                       self.fecha_inicio.strftime('%Y-%m-%d'),
                       self.fecha_fin.strftime('%Y-%m-%d'),
                       self.prima_mensual, self.suma_asegurada,
                       self.tipo_poliza, self.estatus, self.cliente_id)
            cursor.execute(sql, valores)
            conn.commit()
            self.id_poliza = cursor.lastrowid
            print(f"Póliza registrada con ID: {self.id_poliza}")
        except Exception as e:
            print(f"Error al registrar póliza: {e}")
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
            sql = """UPDATE polizas SET
                     numero_poliza=%s, fecha_inicio=%s, fecha_fin=%s,
                     prima_mensual=%s, suma_asegurada=%s,
                     tipo_poliza=%s, estatus=%s, cliente_id=%s
                     WHERE id_poliza=%s"""
            valores = (self.numero_poliza,
                       self.fecha_inicio.strftime('%Y-%m-%d'),
                       self.fecha_fin.strftime('%Y-%m-%d'),
                       self.prima_mensual, self.suma_asegurada,
                       self.tipo_poliza, self.estatus, self.cliente_id, indice)
            cursor.execute(sql, valores)
            conn.commit()
            print("Póliza actualizada correctamente")
        except Exception as e:
            print(f"Error al actualizar póliza: {e}")
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
            cursor.execute("SELECT * FROM polizas")
            filas = cursor.fetchall()
            if not filas:
                print("No hay pólizas registradas.")
            for fila in filas:
                print(fila)
        except Exception as e:
            print(f"Error al consultar pólizas: {e}")
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
            cursor.execute("DELETE FROM polizas WHERE id_poliza=%s", (indice,))
            conn.commit()
            print(f"Póliza con ID {indice} eliminada")
        except Exception as e:
            print(f"Error al eliminar póliza: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
