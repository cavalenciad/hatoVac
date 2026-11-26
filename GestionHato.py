import numpy as np
from Bovino import Bovino
from Vacuna import Vacuna
from Vacunacion import Vacunacion


class GestionHato:
    def __init__(self, nombre_hato, max_bovinos=100, max_vacunas=30):
        self._nombre_hato = str(nombre_hato).strip()
        self._bovinos = np.full(max_bovinos, None, dtype=object)
        self._catalogo_vacunas = np.full(max_vacunas, None, dtype=object)

    def get_nombre_hato(self):
        return self._nombre_hato

    def get_bovinos(self):
        return self._bovinos

    def get_catalogo_vacunas(self):
        return self._catalogo_vacunas

    def _contar_bovinos(self):
        total = 0
        for i in range(len(self._bovinos)):
            if self._bovinos[i] is not None:
                total += 1
        return total

    def _contar_vacunas(self):
        total = 0
        for i in range(len(self._catalogo_vacunas)):
            if self._catalogo_vacunas[i] is not None:
                total += 1
        return total

    def _es_bisiesto(self, anio):
        return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

    def _dias_del_mes(self, mes, anio):
        if mes == 2:
            return 29 if self._es_bisiesto(anio) else 28
        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            return 30
        else:
            return 31

    def _validar_fecha(self, fecha_str):
        partes = str(fecha_str).strip().split("-")
        if len(partes) != 3:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD.")
        if len(partes[0]) != 4 or len(partes[1]) != 2 or len(partes[2]) != 2:
            raise ValueError("La fecha debe tener 4 dígitos para año, 2 para mes y 2 para día.")
        if not (partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit()):
            raise ValueError("La fecha solo debe contener números y guiones.")

        anio = int(partes[0])
        mes = int(partes[1])
        dia = int(partes[2])

        if anio < 1900 or mes < 1 or mes > 12:
            raise ValueError("Año o mes fuera de rango válido.")
        if dia < 1 or dia > self._dias_del_mes(mes, anio):
            raise ValueError(f"El día {dia} no es válido para el mes {mes} del año {anio}.")

    def _sumar_dias_a_fecha(self, fecha_str, dias_a_sumar):
        partes = fecha_str.split("-")
        anio = int(partes[0])
        mes = int(partes[1])
        dia = int(partes[2])

        while dias_a_sumar > 0:
            max_dias = self._dias_del_mes(mes, anio)
            dia += 1
            if dia > max_dias:
                dia = 1
                mes += 1
                if mes > 12:
                    mes = 1
                    anio += 1
            dias_a_sumar -= 1

        mes_str = f"0{mes}" if mes < 10 else str(mes)
        dia_str = f"0{dia}" if dia < 10 else str(dia)
        return f"{anio}-{mes_str}-{dia_str}"

    def _formatear_consecutivo(self, prefijo, numero):
        if numero < 10:
            return f"{prefijo}00{numero}"
        elif numero < 100:
            return f"{prefijo}0{numero}"
        else:
            return f"{prefijo}{numero}"

    def generar_siguiente_id_bovino(self):
        mayor = 0
        for i in range(len(self._bovinos)):
            b = self._bovinos[i]
            if b is not None:
                id_str = b.get_id()
                if len(id_str) > 1 and id_str[0] == "B" and id_str[1:].isdigit():
                    num = int(id_str[1:])
                    if num > mayor:
                        mayor = num
        return self._formatear_consecutivo("B", mayor + 1)

    def generar_siguiente_id_vacuna(self):
        mayor = 0
        for i in range(len(self._catalogo_vacunas)):
            v = self._catalogo_vacunas[i]
            if v is not None:
                id_str = v.get_id()
                if len(id_str) > 1 and id_str[0] == "V" and id_str[1:].isdigit():
                    num = int(id_str[1:])
                    if num > mayor:
                        mayor = num
        return self._formatear_consecutivo("V", mayor + 1)

    def generar_siguiente_id_vacunacion(self):
        mayor = 0
        for i in range(len(self._bovinos)):
            b = self._bovinos[i]
            if b is not None:
                hist = b.get_historial()
                for j in range(len(hist)):
                    reg = hist[j]
                    if reg is not None:
                        id_str = reg.get_id_vacunacion()
                        if len(id_str) > 3 and id_str[:3] == "REG" and id_str[3:].isdigit():
                            num = int(id_str[3:])
                            if num > mayor:
                                mayor = num
        return self._formatear_consecutivo("REG", mayor + 1)

    def buscar_bovino_lineal(self, id_bovino):
        id_buscado = str(id_bovino).strip()
        for i in range(len(self._bovinos)):
            if self._bovinos[i] is not None:
                if self._bovinos[i].get_id() == id_buscado:
                    return self._bovinos[i]
        return None

    def buscar_bovino_binaria(self, id_bovino):
        self.ordenar_bovinos_por_id()
        id_buscado = str(id_bovino).strip()

        inicio = 0
        fin = self._contar_bovinos() - 1

        while inicio <= fin:
            medio = (inicio + fin) // 2
            id_medio = self._bovinos[medio].get_id()

            if id_medio == id_buscado:
                return self._bovinos[medio]
            elif id_medio < id_buscado:
                inicio = medio + 1
            else:
                fin = medio - 1

        return None

    def buscar_vacuna_lineal(self, id_vacuna):
        id_buscado = str(id_vacuna).strip()
        for i in range(len(self._catalogo_vacunas)):
            if self._catalogo_vacunas[i] is not None:
                if self._catalogo_vacunas[i].get_id() == id_buscado:
                    return self._catalogo_vacunas[i]
        return None

    def buscar_vacunacion_por_id(self, id_vacunacion):
            id_buscado = str(id_vacunacion).strip()
            for i in range(len(self._bovinos)):
                bovino = self._bovinos[i]
                if bovino is not None:
                    historial = bovino.get_historial()
                    for j in range(len(historial)):
                        reg = historial[j]
                        if reg is not None and reg.get_id_vacunacion() == id_buscado:
                            return bovino, reg
            return None, None

    def ordenar_bovinos_por_id(self):
        n = self._contar_bovinos()
        for i in range(n - 1):
            indice_menor = i
            for j in range(i + 1, n):
                if self._bovinos[j].get_id() < self._bovinos[indice_menor].get_id():
                    indice_menor = j

            if indice_menor != i:
                temp = self._bovinos[i]
                self._bovinos[i] = self._bovinos[indice_menor]
                self._bovinos[indice_menor] = temp

    def ordenar_vacunaciones_por_proxima_dosis(self, id_bovino):
        bovino = self.buscar_bovino_binaria(id_bovino)
        if bovino is None:
            raise ValueError(f"No existe ningún bovino registrado con el ID '{id_bovino}'.")

        historial = bovino.get_historial()
        n = 0
        for i in range(len(historial)):
            if historial[i] is not None:
                n += 1

        for i in range(n - 1):
            indice_menor = i
            for j in range(i + 1, n):
                fecha_j = historial[j].get_fecha_proxima_dosis()
                fecha_menor = historial[indice_menor].get_fecha_proxima_dosis()
                if fecha_j < fecha_menor:
                    indice_menor = j

            if indice_menor != i:
                temp = historial[i]
                historial[i] = historial[indice_menor]
                historial[indice_menor] = temp

        return historial

    def registrar_bovino(self, nombre, fecha_nacimiento, sexo):
        id_generado = self.generar_siguiente_id_bovino()

        bovino = Bovino(id_generado, nombre, fecha_nacimiento, sexo)
        bovino.set_nombre(nombre)
        bovino.set_fecha_nacimiento(fecha_nacimiento)
        bovino.set_sexo(sexo)

        for i in range(len(self._bovinos)):
            if self._bovinos[i] is None:
                self._bovinos[i] = bovino
                return bovino

        raise ValueError("No hay capacidad disponible en el hato para registrar más bovinos.")
    
    def registrar_vacuna(self, nombre, lote, intervalo_dosis_dias):
        id_generado = self.generar_siguiente_id_vacuna()

        vacuna = Vacuna(id_generado, nombre, lote, intervalo_dosis_dias)
        vacuna.set_nombre(nombre)
        vacuna.set_lote(lote)
        vacuna.set_intervalo_dosis_dias(intervalo_dosis_dias)

        for i in range(len(self._catalogo_vacunas)):
            if self._catalogo_vacunas[i] is None:
                self._catalogo_vacunas[i] = vacuna
                return vacuna

        raise ValueError("El catálogo de vacunas alcanzó su capacidad máxima.")

    def registrar_vacunacion_bovino(self, id_bovino, id_vacuna, fecha_aplicacion, fecha_actual):
        bovino = self.buscar_bovino_binaria(id_bovino)
        if bovino is None:
            raise ValueError(f"No se puede vacunar: el bovino '{id_bovino}' no está registrado.")

        vacuna = self.buscar_vacuna_lineal(id_vacuna)
        if vacuna is None:
            raise ValueError(f"No se puede vacunar: la vacuna '{id_vacuna}' no existe en el catálogo.")

        fecha_app_limpia = str(fecha_aplicacion).strip()
        fecha_act_limpia = str(fecha_actual).strip()
        self._validar_fecha(fecha_app_limpia)
        self._validar_fecha(fecha_act_limpia)

        if fecha_app_limpia > fecha_act_limpia:
            raise ValueError("La fecha de aplicación no puede ser futura respecto a la fecha actual.")

        id_generado = self.generar_siguiente_id_vacunacion()
        vacunacion = Vacunacion(id_generado, vacuna, fecha_app_limpia)
        bovino.agregar_vacunacion(vacunacion)
        return vacunacion

    def editar_bovino(self, id_bovino, nuevo_nombre=None, nueva_fecha_nac=None, nuevo_sexo=None):
        bovino = self.buscar_bovino_binaria(id_bovino)
        if bovino is None:
            raise ValueError(f"No existe ningún bovino registrado con el ID '{id_bovino}'.")

        # Validar coherencia de la nueva fecha de nacimiento con su historial existente
        if nueva_fecha_nac is not None and str(nueva_fecha_nac).strip() != "":
            fecha_limpia = str(nueva_fecha_nac).strip()
            self._validar_fecha(fecha_limpia)

            historial = bovino.get_historial()
            for i in range(len(historial)):
                reg = historial[i]
                if reg is not None and fecha_limpia > reg.get_fecha_aplicacion():
                    raise ValueError(
                        f"La fecha de nacimiento ({fecha_limpia}) no puede ser posterior "
                        f"a una vacunación ya registrada ({reg.get_fecha_aplicacion()})."
                    )
            bovino.set_fecha_nacimiento(fecha_limpia)

        if nuevo_nombre is not None and str(nuevo_nombre).strip() != "":
            bovino.set_nombre(nuevo_nombre)

        if nuevo_sexo is not None and str(nuevo_sexo).strip() != "":
            bovino.set_sexo(nuevo_sexo)

        return bovino

    def editar_vacuna(self, id_vacuna, nuevo_nombre=None, nuevo_lote=None, nuevo_intervalo=None):
        vacuna = self.buscar_vacuna_lineal(id_vacuna)
        if vacuna is None:
            raise ValueError(f"No existe ninguna vacuna registrada con el ID '{id_vacuna}'.")

        if nuevo_nombre is not None and str(nuevo_nombre).strip() != "":
            vacuna.set_nombre(nuevo_nombre)

        if nuevo_lote is not None and str(nuevo_lote).strip() != "":
            vacuna.set_lote(nuevo_lote)

        # Solo afecta futuras vacunaciones; no recalcula las ya registradas
        if nuevo_intervalo is not None and str(nuevo_intervalo).strip() != "":
            vacuna.set_intervalo_dosis_dias(int(nuevo_intervalo))

        return vacuna

    def editar_vacunacion(self, id_vacunacion, nuevo_id_vacuna=None, nueva_fecha_aplicacion=None, fecha_actual=None):
        bovino, reg = self.buscar_vacunacion_por_id(id_vacunacion)
        if reg is None:
            raise ValueError(f"No existe ningún registro de vacunación con el ID '{id_vacunacion}'.")

        vacuna_objetivo = reg.get_vacuna()
        if nuevo_id_vacuna is not None and str(nuevo_id_vacuna).strip() != "":
            vacuna_encontrada = self.buscar_vacuna_lineal(nuevo_id_vacuna)
            if vacuna_encontrada is None:
                raise ValueError(f"La vacuna '{nuevo_id_vacuna}' no existe en el catálogo.")
            vacuna_objetivo = vacuna_encontrada

        fecha_objetivo = reg.get_fecha_aplicacion()
        if nueva_fecha_aplicacion is not None and str(nueva_fecha_aplicacion).strip() != "":
            fecha_limpia = str(nueva_fecha_aplicacion).strip()
            self._validar_fecha(fecha_limpia)

            if fecha_actual is not None and fecha_limpia > fecha_actual:
                raise ValueError("La fecha de aplicación no puede ser futura respecto a la fecha actual.")
            if fecha_limpia < bovino.get_fecha_nacimiento():
                raise ValueError(
                    f"La fecha de aplicación ({fecha_limpia}) no puede ser anterior "
                    f"al nacimiento del bovino ({bovino.get_fecha_nacimiento()})."
                )
            fecha_objetivo = fecha_limpia

        # Aplicar cambios y recalcular automáticamente la próxima dosis
        reg.set_vacuna(vacuna_objetivo)
        reg.set_fecha_aplicacion(fecha_objetivo)
        return reg

    def generar_matriz_sanitaria(self, fecha_actual):
        self._validar_fecha(fecha_actual)
        self.ordenar_bovinos_por_id()

        num_bovinos = self._contar_bovinos()
        num_vacunas = self._contar_vacunas()

        if num_bovinos == 0 or num_vacunas == 0:
            raise ValueError("Se requiere al menos un bovino y una vacuna para generar la matriz.")

        matriz = np.full((num_bovinos, num_vacunas), "PENDIENTE", dtype=object)
        fecha_limite_alerta = self._sumar_dias_a_fecha(fecha_actual, 15)

        for i in range(num_bovinos):
            bovino = self._bovinos[i]
            historial = bovino.get_historial()

            for j in range(num_vacunas):
                vacuna = self._catalogo_vacunas[j]
                id_vac = vacuna.get_id()

                ultima_aplicacion = None
                for k in range(len(historial)):
                    reg = historial[k]
                    if reg is not None and reg.get_vacuna().get_id() == id_vac:
                        if ultima_aplicacion is None or reg.get_fecha_aplicacion() > ultima_aplicacion.get_fecha_aplicacion():
                            ultima_aplicacion = reg

                if ultima_aplicacion is None:
                    matriz[i][j] = "PENDIENTE"
                else:
                    fecha_prox = ultima_aplicacion.get_fecha_proxima_dosis()
                    if fecha_prox < fecha_actual:
                        matriz[i][j] = "VENCIDA"
                    elif fecha_prox <= fecha_limite_alerta:
                        matriz[i][j] = "PENDIENTE"
                    else:
                        matriz[i][j] = "APLICADA"

        return matriz

    def imprimir_matriz_sanitaria(self, fecha_actual):
        matriz = self.generar_matriz_sanitaria(fecha_actual)
        num_bovinos = self._contar_bovinos()
        num_vacunas = self._contar_vacunas()

        encabezado = "BOVINO \\ VACUNA\t"
        for j in range(num_vacunas):
            encabezado += f"{self._catalogo_vacunas[j].get_id()}\t\t"
        print(encabezado)
        print("-" * (18 + num_vacunas * 16))

        for i in range(num_bovinos):
            fila_str = f"{self._bovinos[i].get_id()} ({self._bovinos[i].get_nombre()})\t"
            for j in range(num_vacunas):
                fila_str += f"{matriz[i][j]}\t"
            print(fila_str)

    def guardar_datos(self, arch_bovinos="bovinos.txt", arch_vacunas="vacunas.txt", arch_vacunaciones="vacunaciones.txt"):
        with open(arch_bovinos, "w", encoding="utf-8") as f_bov:
            for i in range(len(self._bovinos)):
                b = self._bovinos[i]
                if b is not None:
                    f_bov.write(f"{b.get_id()};{b.get_nombre()};{b.get_fecha_nacimiento()};{b.get_sexo()}\n")

        with open(arch_vacunas, "w", encoding="utf-8") as f_vac:
            for i in range(len(self._catalogo_vacunas)):
                v = self._catalogo_vacunas[i]
                if v is not None:
                    f_vac.write(f"{v.get_id()};{v.get_nombre()};{v.get_lote()};{v.get_intervalo_dosis_dias()}\n")

        with open(arch_vacunaciones, "w", encoding="utf-8") as f_reg:
            for i in range(len(self._bovinos)):
                b = self._bovinos[i]
                if b is not None:
                    hist = b.get_historial()
                    for j in range(len(hist)):
                        reg = hist[j]
                        if reg is not None:
                            f_reg.write(
                                f"{reg.get_id_vacunacion()};"
                                f"{b.get_id()};"
                                f"{reg.get_vacuna().get_id()};"
                                f"{reg.get_fecha_aplicacion()};"
                                f"{reg.get_fecha_proxima_dosis()}\n"
                            )

    def cargar_datos(self, arch_bovinos="bovinos.txt", arch_vacunas="vacunas.txt", arch_vacunaciones="vacunaciones.txt"):
        backup_bovinos = np.full(len(self._bovinos), None, dtype=object)
        backup_vacunas = np.full(len(self._catalogo_vacunas), None, dtype=object)

        cant_bov = 0
        with open(arch_bovinos, "r", encoding="utf-8") as f_bov:
            for linea in f_bov:
                linea = linea.rstrip("\n")
                if linea.strip() != "":
                    if cant_bov >= len(backup_bovinos):
                        raise ValueError("El archivo supera la capacidad máxima de bovinos.")
                    datos = linea.split(";")
                    if len(datos) != 4:
                        raise ValueError("Cada bovino en el archivo debe tener 4 atributos.")
                    b = Bovino(datos[0], datos[1], datos[2], datos[3])
                    b.set_fecha_nacimiento(datos[2])
                    b.set_sexo(datos[3])
                    backup_bovinos[cant_bov] = b
                    cant_bov += 1

        cant_vac = 0
        with open(arch_vacunas, "r", encoding="utf-8") as f_vac:
            for linea in f_vac:
                linea = linea.rstrip("\n")
                if linea.strip() != "":
                    if cant_vac >= len(backup_vacunas):
                        raise ValueError("El archivo supera la capacidad máxima de vacunas.")
                    datos = linea.split(";")
                    if len(datos) != 4:
                        raise ValueError("Cada vacuna en el archivo debe tener 4 atributos.")
                    v = Vacuna(datos[0], datos[1], datos[2], int(datos[3]))
                    v.set_intervalo_dosis_dias(int(datos[3]))
                    backup_vacunas[cant_vac] = v
                    cant_vac += 1

        self._bovinos = backup_bovinos
        self._catalogo_vacunas = backup_vacunas

        with open(arch_vacunaciones, "r", encoding="utf-8") as f_reg:
            for linea in f_reg:
                linea = linea.rstrip("\n")
                if linea.strip() != "":
                    datos = linea.split(";")
                    if len(datos) != 5:
                        raise ValueError("Cada registro de vacunación debe tener 5 atributos.")
                    id_reg, id_bov, id_vac, fecha_app, fecha_prox = datos
                    bovino = self.buscar_bovino_lineal(id_bov)
                    vacuna = self.buscar_vacuna_lineal(id_vac)
                    if bovino is None or vacuna is None:
                        raise ValueError(f"Referencia inválida en vacunación '{id_reg}'.")
                    reg = Vacunacion(id_reg, vacuna, fecha_app, fecha_prox)
                    bovino.agregar_vacunacion(reg)