from PersonaBase import PersonaBase
from conexion import obtener_conexion

class Beneficiario(PersonaBase):

    def __init__(self):
        super().__init__()
        self.id_beneficiario = 0
        self.parentesco = ""
        self.porcentaje_asignado = 0.0
        self.poliza_id = 0

    def ingresar_datos(self):
        super().ingresar_datos()

        self.parentesco = input("Parentesco: ").strip()
        while not self.parentesco:
            print("Error: el parentesco no puede estar vacío.")
            self.parentesco = input("Parentesco: ").strip()

        while True:
            try:
                valor = input("Porcentaje asignado (0-100): ").strip()
                if not valor:
                    print("Error: el porcentaje no puede estar vacío.")
                    continue
                self.porcentaje_asignado = float(valor)
                if self.porcentaje_asignado <= 0:
                    print("Error: el porcentaje debe ser mayor a 0.")
                    continue
                if self.porcentaje_asignado > 100:
                    print("Error: el porcentaje no puede ser mayor a 100.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número válido (ej: 50.5).")

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
        return super().obtener_datos() + \
               f", {self.parentesco}, {self.porcentaje_asignado}, {self.poliza_id}"

    def registrar(self, dato=None):
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO beneficiarios
                     (nombre, apellidos, fecha_nacimiento, parentesco, porcentaje_asignado, poliza_id)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (self.nombre, self.apellidos, self.fecha_nacimiento,
                       self.parentesco, self.porcentaje_asignado, self.poliza_id)
            cursor.execute(sql, valores)
            conn.commit()
            self.id_beneficiario = cursor.lastrowid
            print(f"Beneficiario registrado con ID: {self.id_beneficiario}")
        except Exception as e:
            print(f"Error al registrar beneficiario: {e}")
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
            sql = """UPDATE beneficiarios SET
                     nombre=%s, apellidos=%s, fecha_nacimiento=%s,
                     parentesco=%s, porcentaje_asignado=%s, poliza_id=%s
                     WHERE id_beneficiario=%s"""
            valores = (self.nombre, self.apellidos, self.fecha_nacimiento,
                       self.parentesco, self.porcentaje_asignado, self.poliza_id, indice)
            cursor.execute(sql, valores)
            conn.commit()
            print("Beneficiario actualizado correctamente")
        except Exception as e:
            print(f"Error al actualizar beneficiario: {e}")
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
            cursor.execute("SELECT * FROM beneficiarios")
            filas = cursor.fetchall()
            if not filas:
                print("No hay beneficiarios registrados.")
            for fila in filas:
                print(fila)
        except Exception as e:
            print(f"Error al consultar beneficiarios: {e}")
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
            cursor.execute("DELETE FROM beneficiarios WHERE id_beneficiario=%s", (indice,))
            conn.commit()
            print(f"Beneficiario con ID {indice} eliminado")
        except Exception as e:
            print(f"Error al eliminar beneficiario: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
