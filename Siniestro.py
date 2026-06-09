from OperacionRegistro import OperacionRegistro
from conexion import obtener_conexion
from datetime import datetime

class Siniestro(OperacionRegistro):

    def __init__(self):
        super().__init__()
        self.fecha_reporte = ""
        self.fecha_ocurrencia = ""
        self.tipo_siniestro = ""
        self.monto_reclamado = 0.0
        self.monto_aprobado = 0.0
        self.estatus_siniestro = ""
        self.poliza_id = 0

    def ingresar_datos(self):
        while True:
            fecha_str = input("Fecha reporte (DD/MM/YYYY): ").strip()
            if not fecha_str:
                print("Error: la fecha de reporte no puede estar vacía.")
                continue
            try:
                self.fecha_reporte = datetime.strptime(fecha_str, "%d/%m/%Y")
                break
            except ValueError:
                print("Error: formato de fecha inválido. Usa DD/MM/YYYY (ej: 15/05/2024).")

        while True:
            fecha_str = input("Fecha ocurrencia (DD/MM/YYYY): ").strip()
            if not fecha_str:
                print("Error: la fecha de ocurrencia no puede estar vacía.")
                continue
            try:
                self.fecha_ocurrencia = datetime.strptime(fecha_str, "%d/%m/%Y")
                if self.fecha_ocurrencia > self.fecha_reporte:
                    print("Error: la fecha de ocurrencia no puede ser posterior a la de reporte.")
                    continue
                break
            except ValueError:
                print("Error: formato de fecha inválido. Usa DD/MM/YYYY (ej: 10/05/2024).")

        self.tipo_siniestro = input("Tipo de siniestro: ").strip()
        while not self.tipo_siniestro:
            print("Error: el tipo de siniestro no puede estar vacío.")
            self.tipo_siniestro = input("Tipo de siniestro: ").strip()

        while True:
            try:
                valor = input("Monto reclamado: ").strip()
                if not valor:
                    print("Error: el monto reclamado no puede estar vacío.")
                    continue
                self.monto_reclamado = float(valor)
                if self.monto_reclamado <= 0:
                    print("Error: el monto reclamado debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número válido (ej: 50000.00).")

        while True:
            try:
                valor = input("Monto aprobado: ").strip()
                if not valor:
                    print("Error: el monto aprobado no puede estar vacío.")
                    continue
                self.monto_aprobado = float(valor)
                if self.monto_aprobado < 0:
                    print("Error: el monto aprobado no puede ser negativo.")
                    continue
                if self.monto_aprobado > self.monto_reclamado:
                    print(f"Error: el monto aprobado ({self.monto_aprobado}) no puede superar al reclamado ({self.monto_reclamado}).")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número válido (ej: 45000.00).")

        self.estatus_siniestro = input("Estatus del siniestro: ").strip()
        while not self.estatus_siniestro:
            print("Error: el estatus no puede estar vacío.")
            self.estatus_siniestro = input("Estatus del siniestro: ").strip()

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
        return (f"{self.fecha_reporte.strftime('%Y-%m-%d')}, {self.fecha_ocurrencia.strftime('%Y-%m-%d')}, "
                f"{self.tipo_siniestro}, {self.monto_reclamado}, {self.monto_aprobado}, "
                f"{self.estatus_siniestro}, {self.poliza_id}")

    def procesar(self):
        if self.monto_reclamado <= 0:
            print("Error: el monto reclamado debe ser mayor a 0.")
            return False
        if self.monto_aprobado > self.monto_reclamado:
            print("Error: el monto aprobado supera al reclamado.")
            return False
        print("Siniestro procesado correctamente.")
        return True

    def registrar(self, dato=None):
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO siniestros
                     (fecha_reporte, fecha_ocurrencia, tipo_siniestro,
                      monto_reclamado, monto_aprobado, estatus_siniestro, poliza_id)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (self.fecha_reporte.strftime('%Y-%m-%d'),
                       self.fecha_ocurrencia.strftime('%Y-%m-%d'),
                       self.tipo_siniestro, self.monto_reclamado,
                       self.monto_aprobado, self.estatus_siniestro, self.poliza_id)
            cursor.execute(sql, valores)
            conn.commit()
            self.id = cursor.lastrowid
            print(f"Siniestro registrado con ID: {self.id}")
        except Exception as e:
            print(f"Error al registrar siniestro: {e}")
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
            sql = """UPDATE siniestros SET
                     fecha_reporte=%s, fecha_ocurrencia=%s, tipo_siniestro=%s,
                     monto_reclamado=%s, monto_aprobado=%s,
                     estatus_siniestro=%s, poliza_id=%s
                     WHERE id_siniestro=%s"""
            valores = (self.fecha_reporte.strftime('%Y-%m-%d'),
                       self.fecha_ocurrencia.strftime('%Y-%m-%d'),
                       self.tipo_siniestro, self.monto_reclamado,
                       self.monto_aprobado, self.estatus_siniestro,
                       self.poliza_id, indice)
            cursor.execute(sql, valores)
            conn.commit()
            print("Siniestro actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar siniestro: {e}")
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
            cursor.execute("SELECT * FROM siniestros")
            filas = cursor.fetchall()
            if not filas:
                print("No hay siniestros registrados.")
            for fila in filas:
                print(fila)
        except Exception as e:
            print(f"Error al consultar siniestros: {e}")
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
            cursor.execute("DELETE FROM siniestros WHERE id_siniestro=%s", (indice,))
            conn.commit()
            print(f"Siniestro con ID {indice} eliminado.")
        except Exception as e:
            print(f"Error al eliminar siniestro: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
