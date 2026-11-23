class Vacuna:
    def __init__(self, id_vacuna, nombre, lote, intervalo_dosis_dias):
        self._id = str(id_vacuna).strip()
        self._nombre = str(nombre).strip()
        self._lote = str(lote).strip()
        self._intervalo_dosis_dias = int(intervalo_dosis_dias)

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_lote(self):
        return self._lote

    def get_intervalo_dosis_dias(self):
        return int(self._intervalo_dosis_dias)

    def set_id(self, id_vacuna):
        if id_vacuna is None or str(id_vacuna).strip() == "":
            raise ValueError("El ID de la vacuna no puede estar vacío")
        self._id = str(id_vacuna).strip()

    def set_nombre(self, nombre):
        if nombre is None or str(nombre).strip() == "":
            raise ValueError("El nombre de la vacuna no puede estar vacío")
        self._nombre = str(nombre).strip()

    def set_lote(self, lote):
        if lote is None or str(lote).strip() == "":
            raise ValueError("El lote de la vacuna no puede estar vacío")
        self._lote = str(lote).strip()

    def set_intervalo_dosis_dias(self, intervalo):
        if int(intervalo) < 0:
            raise ValueError("El intervalo en días no puede ser un valor negativo")
        self._intervalo_dosis_dias = int(intervalo)

    def __str__(self):
        return (
            f"ID: {self._id}, nombre: {self._nombre}, "
            f"lote: {self._lote}, intervalo de dosis: {self._intervalo_dosis_dias} días"
        )