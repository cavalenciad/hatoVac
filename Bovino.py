import numpy as np

class Bovino:
    def __init__(self, id_bovino, nombre, fecha_nacimiento, sexo, capacidad_vacunas=20):
        self._id = str(id_bovino).strip()
        self._nombre = str(nombre).strip()
        self._fecha_nacimiento = str(fecha_nacimiento).strip()
        self._sexo = str(sexo).strip().upper()
        self._historial_vacunacion = np.full(capacidad_vacunas, None, dtype=object)

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

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_fecha_nacimiento(self):
        return self._fecha_nacimiento

    def get_edad_meses(self, fecha_actual):
        fecha_act_str = str(fecha_actual).strip()
        self._validar_fecha(fecha_act_str)

        if fecha_act_str < self._fecha_nacimiento:
            raise ValueError("La fecha actual no puede ser anterior a la fecha de nacimiento del bovino.")

        p_nac = self._fecha_nacimiento.split("-")
        p_act = fecha_act_str.split("-")

        meses = (int(p_act[0]) - int(p_nac[0])) * 12 + (int(p_act[1]) - int(p_nac[1]))
        if int(p_act[2]) < int(p_nac[2]):
            meses -= 1

        return meses

    def get_sexo(self):
        return self._sexo

    def get_historial(self):
        return self._historial_vacunacion

    # --- SETTERS ---
    def set_id(self, id_bovino):
        if not id_bovino or str(id_bovino).strip() == "":
            raise ValueError("El ID del bovino no puede estar vacío.")
        self._id = str(id_bovino).strip()

    def set_nombre(self, nombre):
        if not nombre or str(nombre).strip() == "":
            raise ValueError("El nombre del bovino no puede estar vacío.")
        self._nombre = str(nombre).strip()

    def set_fecha_nacimiento(self, fecha_nacimiento):
        fecha_str = str(fecha_nacimiento).strip()
        self._validar_fecha(fecha_str)
        self._fecha_nacimiento = fecha_str

    def set_sexo(self, sexo):
        sexo_norm = str(sexo).strip().upper()
        if sexo_norm not in ["M", "H"]:
            raise ValueError("El sexo debe ser 'M' (Macho) o 'H' (Hembra).")
        self._sexo = sexo_norm

    def agregar_vacunacion(self, vacunacion):
        if vacunacion.get_fecha_aplicacion() < self._fecha_nacimiento:
            raise ValueError(
                f"La fecha de vacunación ({vacunacion.get_fecha_aplicacion()}) no puede ser "
                f"anterior a la fecha de nacimiento del bovino ({self._fecha_nacimiento})."
            )

        for i in range(len(self._historial_vacunacion)):
            if self._historial_vacunacion[i] is None:
                self._historial_vacunacion[i] = vacunacion
                return True

        raise ValueError(f"El historial del bovino {self._id} alcanzó su capacidad máxima.")

    def __str__(self):
        total_vacunas = 0
        for i in range(len(self._historial_vacunacion)):
            if self._historial_vacunacion[i] is not None:
                total_vacunas += 1

        return (
            f"ID: {self._id} | Nombre: {self._nombre} | "
            f"Nacimiento: {self._fecha_nacimiento} | Sexo: {self._sexo} | "
            f"Vacunas aplicadas: {total_vacunas}"
        )