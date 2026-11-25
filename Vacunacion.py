class Vacunacion:
    def __init__(self, id_vacunacion, vacuna, fecha_aplicacion, fecha_proxima_dosis=None):
        self._id_vacunacion = str(id_vacunacion).strip()
        self._vacuna = vacuna
        self._fecha_aplicacion = str(fecha_aplicacion).strip()

        if fecha_proxima_dosis is not None and str(fecha_proxima_dosis).strip() != "":
            self._fecha_proxima_dosis = str(fecha_proxima_dosis).strip()
        else:
            self._fecha_proxima_dosis = self._calcular_proxima_dosis()

    def _es_bisiesto(self, anio):
        return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

    def _dias_del_mes(self, mes, anio):
        if mes == 2:
            if self._es_bisiesto(anio):
                return 29
            else:
                return 28
        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            return 30
        else:
            return 31

    def _validar_y_descomponer_fecha(self, fecha_str):
        partes = fecha_str.split("-")
        if len(partes) != 3:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD.")

        if len(partes[0]) != 4 or len(partes[1]) != 2 or len(partes[2]) != 2:
            raise ValueError("La fecha debe tener exactamente 4 dígitos para el año, 2 para el mes y 2 para el día.")

        if not (partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit()):
            raise ValueError("La fecha solo puede contener números y guiones.")

        anio = int(partes[0])
        mes = int(partes[1])
        dia = int(partes[2])

        if anio < 1900 or mes < 1 or mes > 12:
            raise ValueError("Año o mes fuera de rango válido.")

        max_dias = self._dias_del_mes(mes, anio)
        if dia < 1 or dia > max_dias:
            raise ValueError(f"El día {dia} no es válido para el mes {mes} del año {anio}.")

        return anio, mes, dia

    def _formatear_fecha(self, anio, mes, dia):
        mes_str = f"0{mes}" if mes < 10 else str(mes)
        dia_str = f"0{dia}" if dia < 10 else str(dia)
        return f"{anio}-{mes_str}-{dia_str}"

    def _calcular_proxima_dosis(self):
        anio, mes, dia = self._validar_y_descomponer_fecha(self._fecha_aplicacion)
        dias_a_sumar = self._vacuna.get_intervalo_dosis_dias()

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

        return self._formatear_fecha(anio, mes, dia)

    def get_id_vacunacion(self):
        return self._id_vacunacion

    def get_vacuna(self):
        return self._vacuna

    def get_fecha_aplicacion(self):
        return self._fecha_aplicacion

    def get_fecha_proxima_dosis(self):
        return self._fecha_proxima_dosis

    def set_id_vacunacion(self, id_vacunacion):
        if id_vacunacion is None or str(id_vacunacion).strip() == "":
            raise ValueError("El ID de la vacunación no puede estar vacío.")
        self._id_vacunacion = str(id_vacunacion).strip()

    def set_vacuna(self, vacuna):
        if vacuna is None:
            raise ValueError("Debe asociarse una vacuna válida al registro.")
        self._vacuna = vacuna

    def set_fecha_aplicacion(self, fecha_aplicacion):
        fecha_str = str(fecha_aplicacion).strip()
        self._validar_y_descomponer_fecha(fecha_str)
        self._fecha_aplicacion = fecha_str
        self._fecha_proxima_dosis = self._calcular_proxima_dosis() #Por qué aquí y no en el Setter de set_fecha_proxima_dosis

    def set_fecha_proxima_dosis(self, fecha_proxima_dosis):
        fecha_str = str(fecha_proxima_dosis).strip()
        self._validar_y_descomponer_fecha(fecha_str)
        self._fecha_proxima_dosis = fecha_str

    def __str__(self):
        return (
            f"ID Registro: {self._id_vacunacion} | "
            f"Vacuna: {self._vacuna.get_nombre()} (Lote: {self._vacuna.get_lote()}) | "
            f"Aplicada: {self._fecha_aplicacion} | "
            f"Próxima dosis: {self._fecha_proxima_dosis}"
        )