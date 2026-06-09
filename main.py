from Cliente import Cliente
from Beneficiario import Beneficiario
from Poliza import Poliza
from Pago import Pago
from Siniestro import Siniestro
from conexion import obtener_conexion

def eliminar_cliente_completo():
    conn = None
    cursor = None
    try:
        while True:
            try:
                valor = input("ID del cliente a eliminar: ").strip()
                if not valor:
                    print("Error: el ID no puede estar vacío.")
                    continue
                id_cliente = int(valor)
                if id_cliente <= 0:
                    print("Error: el ID debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Error: ingresa un número entero válido.")

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT id_cliente, nombre, apellidos FROM clientes WHERE id_cliente=%s", (id_cliente,))
        cliente = cursor.fetchone()
        if not cliente:
            print(f"Error: no existe un cliente con ID {id_cliente}.")
            return

        print(f"\nCliente encontrado: {cliente[1]} {cliente[2]} (ID: {cliente[0]})")

        cursor.execute("SELECT id_poliza, numero_poliza, tipo_poliza, estatus FROM polizas WHERE cliente_id=%s", (id_cliente,))
        polizas = cursor.fetchall()

        if polizas:
            print(f"\nEste cliente tiene {len(polizas)} póliza(s):")
            total_siniestros = 0
            total_pagos = 0
            total_beneficiarios = 0

            for pol in polizas:
                id_pol = pol[0]
                print(f"  - Póliza #{pol[1]} (ID: {id_pol}, Tipo: {pol[2]}, Estatus: {pol[3]})")

                cursor.execute("SELECT COUNT(*) FROM siniestros WHERE poliza_id=%s", (id_pol,))
                n_sin = cursor.fetchone()[0]
                total_siniestros += n_sin

                cursor.execute("SELECT COUNT(*) FROM pagos WHERE poliza_id=%s", (id_pol,))
                n_pag = cursor.fetchone()[0]
                total_pagos += n_pag

                cursor.execute("SELECT COUNT(*) FROM beneficiarios WHERE poliza_id=%s", (id_pol,))
                n_ben = cursor.fetchone()[0]
                total_beneficiarios += n_ben

                if n_sin > 0 or n_pag > 0 or n_ben > 0:
                    print(f"      → {n_sin} siniestro(s), {n_pag} pago(s), {n_ben} beneficiario(s)")

            print(f"\n⚠️  Se eliminarán en total:")
            print(f"    - {total_beneficiarios} beneficiario(s)")
            print(f"    - {total_pagos} pago(s)")
            print(f"    - {total_siniestros} siniestro(s)")
            print(f"    - {len(polizas)} póliza(s)")
            print(f"    - 1 cliente")
        else:
            print("\nEste cliente no tiene pólizas asociadas.")

        confirmar = input("\n¿Estás seguro de que quieres eliminar todo? (si/no): ").strip().lower()
        if confirmar != "si":
            print("Operación cancelada.")
            return

        for pol in polizas:
            id_pol = pol[0]

            cursor.execute("DELETE FROM siniestros WHERE poliza_id=%s", (id_pol,))
            eliminados = cursor.rowcount
            if eliminados > 0:
                print(f"  ✓ {eliminados} siniestro(s) de póliza {id_pol} eliminado(s)")

            cursor.execute("DELETE FROM pagos WHERE poliza_id=%s", (id_pol,))
            eliminados = cursor.rowcount
            if eliminados > 0:
                print(f"  ✓ {eliminados} pago(s) de póliza {id_pol} eliminado(s)")

            cursor.execute("DELETE FROM beneficiarios WHERE poliza_id=%s", (id_pol,))
            eliminados = cursor.rowcount
            if eliminados > 0:
                print(f"  ✓ {eliminados} beneficiario(s) de póliza {id_pol} eliminado(s)")

        cursor.execute("DELETE FROM polizas WHERE cliente_id=%s", (id_cliente,))
        eliminados = cursor.rowcount
        if eliminados > 0:
            print(f"  ✓ {eliminados} póliza(s) eliminada(s)")

        cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id_cliente,))
        print(f"  ✓ Cliente {cliente[1]} {cliente[2]} (ID: {id_cliente}) eliminado")

        conn.commit()
        print(f"\n✅ Cliente y todos sus registros eliminados exitosamente.")

    except Exception as e:
        print(f"Error al eliminar cliente: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def menu_principal():
    while True:
        print("\n" + "="*50)
        print("   SISTEMA DE ASEGURADORA")
        print("="*50)
        print("1. Registrar Cliente")
        print("2. Registrar Póliza")
        print("3. Registrar Beneficiario")
        print("4. Registrar Pago")
        print("5. Registrar Siniestro")
        print("6. Consultar Clientes")
        print("7. Consultar Pólizas")
        print("8. Consultar Beneficiarios")
        print("9. Consultar Pagos")
        print("10. Consultar Siniestros")
        print("11. Eliminar Cliente (y todo lo relacionado)")
        print("0. Salir")
        print("="*50)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR CLIENTE ---")
            c = Cliente()
            c.ingresar_datos()
            c.registrar()
            print("Datos guardados:", c.obtener_datos())

        elif opcion == "2":
            print("\n--- REGISTRAR PÓLIZA ---")
            p = Poliza()
            p.ingresar_datos()
            p.registrar()
            print("Datos guardados:", p.obtener_datos())

        elif opcion == "3":
            print("\n--- REGISTRAR BENEFICIARIO ---")
            b = Beneficiario()
            b.ingresar_datos()
            b.registrar()
            print("Datos guardados:", b.obtener_datos())

        elif opcion == "4":
            print("\n--- REGISTRAR PAGO ---")
            pg = Pago()
            pg.ingresar_datos()
            if pg.procesar():
                pg.registrar()
            print("Datos guardados:", pg.obtener_datos())

        elif opcion == "5":
            print("\n--- REGISTRAR SINIESTRO ---")
            s = Siniestro()
            s.ingresar_datos()
            if s.procesar():
                s.registrar()
            print("Datos guardados:", s.obtener_datos())

        elif opcion == "6":
            print("\n--- CLIENTES REGISTRADOS ---")
            Cliente().consultar()

        elif opcion == "7":
            print("\n--- PÓLIZAS REGISTRADAS ---")
            Poliza().consultar()

        elif opcion == "8":
            print("\n--- BENEFICIARIOS REGISTRADOS ---")
            Beneficiario().consultar()

        elif opcion == "9":
            print("\n--- PAGOS REGISTRADOS ---")
            Pago().consultar()

        elif opcion == "10":
            print("\n--- SINIESTROS REGISTRADOS ---")
            Siniestro().consultar()

        elif opcion == "11":
            print("\n--- ELIMINAR CLIENTE ---")
            print("Clientes actuales:")
            Cliente().consultar()
            print()
            eliminar_cliente_completo()

        elif opcion == "0":
            print("\n¡Hasta luego!")
            break

        else:
            print("\nError: opción no válida. Selecciona un número del menú.")

if __name__ == "__main__":
    menu_principal()
