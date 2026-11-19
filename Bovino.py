import numpy as np

class Bovino:
    def __init__(self, id_bovino, nombre, edad, sexo, capacidad_vacunas=20):
        self._id = str(id_bovino).strip()
        self._nombre = str(nombre).strip()
        self._edad = int(edad)
        self._sexo = str(sexo).strip().upper()
        self._historial_vacunacion = np.full(capacidad_vacunas, None, dtype=object)

    # --- GETTERS ---
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_edad(self):
        return int(self._edad)

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

    def set_edad(self, edad):
        if int(edad) < 0:
            raise ValueError("La edad en meses no puede ser un valor negativo.")
        self._edad = int(edad)

    def set_sexo(self, sexo):
        sexo_norm = str(sexo).strip().upper()
        if sexo_norm not in ["M", "H"]:
            raise ValueError("El sexo debe ser 'M' (Macho) o 'H' (Hembra).")
        self._sexo = sexo_norm

    # --- MÉTODOS DE GESTIÓN DEL HISTORIAL ---
    def agregar_vacunacion(self, vacunacion):
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
            f"Edad: {self._edad} meses | Sexo: {self._sexo} | "
            f"Vacunas aplicadas: {total_vacunas}"
        )