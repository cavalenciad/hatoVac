from GestionHato import GestionHato

RESET = "\033[0m"
NEGRITA = "\033[1m"
CIAN = "\033[96m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
BLANCO = "\033[97m"


def pausar():
    input(f"\n{AMARILLO}Presione Enter para continuar...{RESET}")


def mostrar_menu(nombre_hato, fecha_actual):
    print(f"\n{CIAN}{NEGRITA}======================================================{RESET}")
    print(f"{CIAN}{NEGRITA}   HATOVAC - {nombre_hato.upper()} (Corte: {fecha_actual}){RESET}")
    print(f"{CIAN}{NEGRITA}======================================================{RESET}")
    print(f" {BLANCO}1.{RESET} Registrar nuevo bovino")
    print(f" {BLANCO}2.{RESET} Registrar nueva vacuna en catálogo")
    print(f" {BLANCO}3.{RESET} Registrar aplicación de vacuna a bovino")
    print(f" {BLANCO}4.{RESET} Consultar bovino e historial (Búsqueda Binaria)")
    print(f" {BLANCO}5.{RESET} Listar bovinos ordenados por ID (Selection Sort)")
    print(f" {BLANCO}6.{RESET} Ver matriz de control sanitario")
    print(f" {BLANCO}7.{RESET} Editar registro (Bovino / Vacuna / Vacunación)")
    print(f" {BLANCO}8.{RESET} Guardar datos en archivos (.txt)")
    print(f" {BLANCO}9.{RESET} Recargar datos desde archivos (.txt)")
    print(f" {ROJO}0.{RESET} Salir")
    print(f"{CIAN}======================================================{RESET}")


def imprimir_matriz_estetica(hato, fecha_actual):
    matriz = hato.generar_matriz_sanitaria(fecha_actual)
    bovinos = hato.get_bovinos()
    vacunas = hato.get_catalogo_vacunas()

    num_bovinos = matriz.shape[0]
    num_vacunas = matriz.shape[1]

    ancho_bovino = 20
    ancho_col = 12
    ancho_total = ancho_bovino + 3 + (num_vacunas * (ancho_col + 3))

    print(f"\n{CIAN}{NEGRITA}--- MATRIZ DE CONTROL SANITARIO (Corte: {fecha_actual}) ---{RESET}")
    print(f"{CIAN}{'-' * ancho_total}{RESET}")

    encabezado = f"{CIAN}{NEGRITA}{'BOVINO':<{ancho_bovino}}{RESET} | "
    for j in range(num_vacunas):
        encabezado += f"{CIAN}{NEGRITA}{vacunas[j].get_id():^{ancho_col}}{RESET} | "
    print(encabezado)
    print(f"{CIAN}{'-' * ancho_total}{RESET}")

    for i in range(num_bovinos):
        etiqueta_bovino = f"{bovinos[i].get_id()} ({bovinos[i].get_nombre()})"
        fila = f"{BLANCO}{etiqueta_bovino:<{ancho_bovino}}{RESET} | "

        for j in range(num_vacunas):
            estado = matriz[i][j]
            if estado == "APLICADA":
                color_estado = VERDE
            elif estado == "PENDIENTE":
                color_estado = AMARILLO
            else:
                color_estado = ROJO

            fila += f"{color_estado}{estado:^{ancho_col}}{RESET} | "
        print(fila)

    print(f"{CIAN}{'-' * ancho_total}{RESET}")
    print(f"Leyenda: {VERDE}■ APLICADA (Vigente){RESET}  {AMARILLO}■ PENDIENTE (Sin dosis o <=15 días){RESET}  {ROJO}■ VENCIDA{RESET}")


def gestionar_edicion(hato, fecha_actual):
    print(f"\n{AMARILLO}{NEGRITA}--- EDITAR REGISTRO EXISTENTE ---{RESET}")
    print(f" {BLANCO}1.{RESET} Editar Bovino")
    print(f" {BLANCO}2.{RESET} Editar Vacuna del catálogo")
    print(f" {BLANCO}3.{RESET} Editar Registro de Vacunación")
    print(f" {ROJO}0.{RESET} Volver al menú principal")

    sub_opcion = input(f"\n{NEGRITA}Seleccione qué desea editar: {RESET}").strip()

    if sub_opcion == "1":
        id_bovino = input("Ingrese el ID del bovino a editar: ").strip()
        bovino = hato.buscar_bovino_binaria(id_bovino)
        if bovino is None:
            print(f"{ROJO}No se encontró ningún bovino con el ID '{id_bovino}'.{RESET}")
            return

        print(f"\n{CIAN}Datos actuales:{RESET} {bovino}")
        print(f"{AMARILLO}(Presione Enter para conservar el valor actual){RESET}")
        nuevo_nombre = input(f"Nuevo nombre [{bovino.get_nombre()}]: ")
        nueva_fecha = input(f"Nueva fecha de nacimiento [{bovino.get_fecha_nacimiento()}]: ")
        nuevo_sexo = input(f"Nuevo sexo M/H [{bovino.get_sexo()}]: ")

        bovino_actualizado = hato.editar_bovino(id_bovino, nuevo_nombre, nueva_fecha, nuevo_sexo)
        print(f"{VERDE}Bovino actualizado exitosamente:{RESET} {bovino_actualizado}")

    elif sub_opcion == "2":
        id_vacuna = input("Ingrese el ID de la vacuna a editar: ").strip()
        vacuna = hato.buscar_vacuna_lineal(id_vacuna)
        if vacuna is None:
            print(f"{ROJO}No se encontró ninguna vacuna con el ID '{id_vacuna}'.{RESET}")
            return

        print(f"\n{CIAN}Datos actuales:{RESET} {vacuna}")
        print(f"{AMARILLO}(Presione Enter para conservar el valor actual){RESET}")
        nuevo_nombre = input(f"Nuevo nombre [{vacuna.get_nombre()}]: ")
        nuevo_lote = input(f"Nuevo lote [{vacuna.get_lote()}]: ")
        nuevo_intervalo = input(f"Nuevo intervalo en días [{vacuna.get_intervalo_dosis_dias()}]: ")

        vacuna_actualizada = hato.editar_vacuna(id_vacuna, nuevo_nombre, nuevo_lote, nuevo_intervalo)
        print(f"{VERDE}Vacuna actualizada exitosamente:{RESET} {vacuna_actualizada}")

    elif sub_opcion == "3":
        id_reg = input("Ingrese el ID del registro de vacunación a editar (ej. REG002): ").strip()
        bovino, reg = hato.buscar_vacunacion_por_id(id_reg)
        if reg is None:
            print(f"{ROJO}No se encontró ningún registro de vacunación con el ID '{id_reg}'.{RESET}")
            return

        print(f"\n{CIAN}Bovino asociado:{RESET} {bovino.get_id()} ({bovino.get_nombre()})")
        print(f"{CIAN}Datos actuales:{RESET} {reg}")
        print(f"{AMARILLO}(Presione Enter para conservar el valor actual){RESET}")
        nuevo_id_vac = input(f"Nuevo ID de vacuna [{reg.get_vacuna().get_id()}]: ")
        nueva_fecha_app = input(f"Nueva fecha de aplicación [{reg.get_fecha_aplicacion()}]: ")

        reg_actualizado = hato.editar_vacunacion(id_reg, nuevo_id_vac, nueva_fecha_app, fecha_actual)
        print(f"{VERDE}Registro de vacunación actualizado exitosamente:{RESET}")
        print(f"  {reg_actualizado}")

    elif sub_opcion == "0":
        return
    else:
        print(f"{ROJO}Opción no válida.{RESET}")


def main():
    hato = GestionHato("Finca La Panchita")

    # 1. Carga automática de datos al iniciar el programa
    try:
        hato.cargar_datos()
        print(f"{VERDE}[Sistema]: Datos cargados automáticamente desde los archivos .txt.{RESET}")
    except FileNotFoundError:
        print(f"{AMARILLO}[Sistema]: No se encontraron archivos previos. Iniciando hato vacío.{RESET}")
    except ValueError as e:
        print(f"{ROJO}[Error al cargar archivos]: {e}{RESET}")

    # 2. Solicitar fecha de referencia inicial
    fecha_actual = ""
    fecha_valida = False
    while not fecha_valida:
        try:
            fecha_actual = input(f"\n{CIAN}Ingrese la fecha actual del sistema (AAAA-MM-DD): {RESET}").strip()
            hato._validar_fecha(fecha_actual)
            fecha_valida = True
        except ValueError as e:
            print(f"{ROJO}[Error]: {e}{RESET}")

    salir = False

    while not salir:
        mostrar_menu(hato.get_nombre_hato(), fecha_actual)
        opcion = input(f"{NEGRITA}Seleccione una opción: {RESET}").strip()

        try:
            if opcion == "1":
                siguiente_id = hato.generar_siguiente_id_bovino()
                print(f"\n{AMARILLO}{NEGRITA}--- REGISTRO DE BOVINO (ID Asignado: {siguiente_id}) ---{RESET}")
                nombre = input("Nombre del bovino: ")
                fecha_nac = input("Fecha de nacimiento (AAAA-MM-DD): ")
                sexo = input("Sexo (M para Macho / H para Hembra): ")

                bovino = hato.registrar_bovino(nombre, fecha_nac, sexo)
                print(f"{VERDE}Bovino registrado exitosamente con ID: {NEGRITA}{bovino.get_id()}{RESET}")
                pausar()

            elif opcion == "2":
                siguiente_id = hato.generar_siguiente_id_vacuna()
                print(f"\n{AMARILLO}{NEGRITA}--- REGISTRO DE VACUNA (ID Asignado: {siguiente_id}) ---{RESET}")
                nombre = input("Nombre de la vacuna: ")
                lote = input("Lote: ")
                intervalo = int(input("Intervalo para próxima dosis (en días): "))

                vacuna = hato.registrar_vacuna(nombre, lote, intervalo)
                print(f"{VERDE}Vacuna registrada exitosamente con ID: {NEGRITA}{vacuna.get_id()}{RESET}")
                pausar()

            elif opcion == "3":
                siguiente_id = hato.generar_siguiente_id_vacunacion()
                print(f"\n{AMARILLO}{NEGRITA}--- REGISTRO DE APLICACIÓN DE VACUNA (ID Asignado: {siguiente_id}) ---{RESET}")
                id_bovino = input("ID del bovino a vacunar: ")
                id_vacuna = input("ID de la vacuna aplicada: ")
                fecha_app = input("Fecha de aplicación (AAAA-MM-DD): ")

                reg = hato.registrar_vacunacion_bovino(
                    id_bovino, id_vacuna, fecha_app, fecha_actual
                )
                print(f"{VERDE}Vacunación registrada exitosamente con ID: {NEGRITA}{reg.get_id_vacunacion()}{RESET}")
                print(f"{CIAN}Próxima dosis calculada para: {NEGRITA}{reg.get_fecha_proxima_dosis()}{RESET}")
                pausar()

            elif opcion == "4":
                print(f"\n{AMARILLO}{NEGRITA}--- CONSULTA DE BOVINO E HISTORIAL ---{RESET}")
                id_bovino = input("Ingrese el ID del bovino a buscar: ")
                bovino = hato.buscar_bovino_binaria(id_bovino)

                if bovino is None:
                    print(f"{ROJO}No se encontró ningún bovino con el ID '{id_bovino.strip()}'.{RESET}")
                else:
                    print(f"\n{CIAN}{NEGRITA}Ficha técnica:{RESET}")
                    print(f"  {bovino}")
                    print(f"  {CIAN}Edad calculada a {fecha_actual}:{RESET} {bovino.get_edad_meses(fecha_actual)} meses")

                    historial = hato.ordenar_vacunaciones_por_proxima_dosis(id_bovino)
                    print(f"\n{CIAN}{NEGRITA}Historial de vacunaciones (ordenado por próxima dosis):{RESET}")
                    tiene_vacunas = False
                    for i in range(len(historial)):
                        if historial[i] is not None:
                            print(f"  {VERDE}•{RESET} {historial[i]}")
                            tiene_vacunas = True
                    if not tiene_vacunas:
                        print(f"  {AMARILLO}Este bovino aún no tiene vacunaciones registradas.{RESET}")

                pausar()

            elif opcion == "5":
                print(f"\n{AMARILLO}{NEGRITA}--- LISTADO GENERAL DE BOVINOS (ORDENADOS POR ID) ---{RESET}")
                hato.ordenar_bovinos_por_id()
                bovinos = hato.get_bovinos()
                hay_datos = False
                for i in range(len(bovinos)):
                    if bovinos[i] is not None:
                        print(f"  {CIAN}•{RESET} {bovinos[i]}")
                        hay_datos = True
                if not hay_datos:
                    print(f"{AMARILLO}No hay bovinos registrados en el hato.{RESET}")

                pausar()

            elif opcion == "6":
                imprimir_matriz_estetica(hato, fecha_actual)
                pausar()

            elif opcion == "7":
                gestionar_edicion(hato, fecha_actual)
                pausar()

            elif opcion == "8":
                print(f"\n{AMARILLO}{NEGRITA}--- GUARDANDO DATOS ---{RESET}")
                hato.guardar_datos()
                print(f"{VERDE}Información guardada en 'bovinos.txt', 'vacunas.txt' y 'vacunaciones.txt'.{RESET}")
                pausar()

            elif opcion == "9":
                print(f"\n{AMARILLO}{NEGRITA}--- RECARGANDO DATOS ---{RESET}")
                hato.cargar_datos()
                print(f"{VERDE}Información recargada exitosamente desde los archivos.{RESET}")
                pausar()

            elif opcion == "0":
                respuesta = input(f"\n{AMARILLO}¿Desea guardar los cambios antes de salir? (S/N): {RESET}").strip().upper()
                if respuesta == "S":
                    hato.guardar_datos()
                    print(f"{VERDE}Datos guardados.{RESET}")
                print(f"{CIAN}Saliendo de HatoVac...{RESET}")
                salir = True

            else:
                print(f"{ROJO}Opción no válida. Por favor seleccione un número del 0 al 9.{RESET}")
                pausar()

        except ValueError as e:
            print(f"\n{ROJO}[Error de validación]: {e}{RESET}")
            pausar()
        except FileNotFoundError:
            print(f"\n{ROJO}[Error de archivo]: No se encontraron los archivos de datos guardados aún.{RESET}")
            pausar()


main()