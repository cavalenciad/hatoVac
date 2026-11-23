from GestionHato import GestionHato


def mostrar_menu():
    print("\n==========================================")
    print("   HATOVAC - GESTIÓN DE VACUNACIÓN BOVINA")
    print("==========================================")
    print("1. Registrar nuevo bovino")
    print("2. Registrar nueva vacuna en catálogo")
    print("3. Registrar aplicación de vacuna a bovino")
    print("4. Consultar bovino e historial (Búsqueda Binaria)")
    print("5. Listar bovinos ordenados por ID (Selection Sort)")
    print("6. Ver matriz de control sanitario (Aplicada/Pendiente/Vencida)")
    print("7. Guardar datos en archivos (.txt)")
    print("8. Cargar datos desde archivos (.txt)")
    print("0. Salir")
    print("==========================================")


def main():
    hato = GestionHato("Hacienda El Progreso")

    fecha_actual = ""
    fecha_valida = False
    while not fecha_valida:
        try:
            fecha_actual = input("Ingrese la fecha actual del sistema (AAAA-MM-DD): ").strip()
            hato._validar_fecha(fecha_actual)
            fecha_valida = True
        except ValueError as e:
            print(f"Error: {e}")

    salir = False

    while not salir:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                print("\n--- REGISTRO DE BOVINO ---")
                id_bovino = input("ID del bovino (ej. B001): ")
                nombre = input("Nombre del bovino: ")
                fecha_nac = input("Fecha de nacimiento (AAAA-MM-DD): ")
                sexo = input("Sexo (M para Macho / H para Hembra): ")

                hato.registrar_bovino(id_bovino, nombre, fecha_nac, sexo)
                print("Bovino registrado exitosamente.")

            elif opcion == "2":
                print("\n--- REGISTRO DE VACUNA ---")
                id_vacuna = input("ID de la vacuna (ej. V001): ")
                nombre = input("Nombre de la vacuna: ")
                lote = input("Lote: ")
                intervalo = int(input("Intervalo para próxima dosis (en días): "))

                hato.registrar_vacuna(id_vacuna, nombre, lote, intervalo)
                print("Vacuna registrada exitosamente en el catálogo.")

            elif opcion == "3":
                print("\n--- REGISTRO DE APLICACIÓN DE VACUNA ---")
                id_vacunacion = input("Código del registro de vacunación (ej. REG01): ")
                id_bovino = input("ID del bovino a vacunar: ")
                id_vacuna = input("ID de la vacuna aplicada: ")
                fecha_app = input("Fecha de aplicación (AAAA-MM-DD): ")

                reg = hato.registrar_vacunacion_bovino(
                    id_vacunacion, id_bovino, id_vacuna, fecha_app, fecha_actual
                )
                print("Vacunación registrada exitosamente.")
                print(f"Próxima dosis calculada para: {reg.get_fecha_proxima_dosis()}")

            elif opcion == "4":
                print("\n--- CONSULTA DE BOVINO E HISTORIAL ---")
                id_bovino = input("Ingrese el ID del bovino a buscar: ")
                bovino = hato.buscar_bovino_binaria(id_bovino)

                if bovino is None:
                    print(f"No se encontró ningún bovino con el ID '{id_bovino.strip()}'.")
                else:
                    print("\nFicha técnica:")
                    print(bovino)
                    print(f"Edad calculada a {fecha_actual}: {bovino.get_edad_meses(fecha_actual)} meses")

                    historial = hato.ordenar_vacunaciones_por_proxima_dosis(id_bovino)
                    print("\nHistorial de vacunaciones (ordenado por próxima dosis):")
                    tiene_vacunas = False
                    for i in range(len(historial)):
                        if historial[i] is not None:
                            print(f"  - {historial[i]}")
                            tiene_vacunas = True
                    if not tiene_vacunas:
                        print("  Este bovino aún no tiene vacunaciones registradas.")

            elif opcion == "5":
                print("\n--- LISTADO GENERAL DE BOVINOS (ORDENADOS POR ID) ---")
                hato.ordenar_bovinos_por_id()
                bovinos = hato.get_bovinos()
                hay_datos = False
                for i in range(len(bovinos)):
                    if bovinos[i] is not None:
                        print(f"  {bovinos[i]}")
                        hay_datos = True
                if not hay_datos:
                    print("No hay bovinos registrados en el hato.")

            elif opcion == "6":
                print(f"\n--- MATRIZ DE CONTROL SANITARIO (Corte: {fecha_actual}) ---")
                hato.imprimir_matriz_sanitaria(fecha_actual)

            elif opcion == "7":
                print("\n--- GUARDANDO DATOS ---")
                hato.guardar_datos()
                print("Información guardada en 'bovinos.txt', 'vacunas.txt' y 'vacunaciones.txt'.")

            elif opcion == "8":
                print("\n--- CARGANDO DATOS ---")
                hato.cargar_datos()
                print("Información cargada exitosamente desde los archivos.")

            elif opcion == "0":
                respuesta = input("¿Desea guardar los cambios antes de salir? (S/N): ").strip().upper()
                if respuesta == "S":
                    hato.guardar_datos()
                    print("Datos guardados.")
                print("Saliendo de HatoVac...")
                salir = True

            else:
                print("Opción no válida. Por favor seleccione un número del 0 al 8.")

        except ValueError as e:
            print(f"\n[Error de validación]: {e}")
        except FileNotFoundError:
            print("\n[Error de archivo]: No se encontraron los archivos de datos guardados aún.")


main()