from datetime import datetime, timedelta

class Vacunacion:
    def __init__(self, id_vacunacion, vacuna, fecha_aplicacion, fecha_proxima_dosis=None):
        self._id_vacunacion = str(id_vacunacion).strip()
        self._vacuna = vacuna  # Objeto de tipo Vacuna (relación 1 a 1 del diagrama)
        self._fecha_aplicacion = str(fecha_aplicacion).strip()
        
        if fecha_proxima_dosis is not None and str(fecha_proxima_dosis).strip() != "":
            self._fecha_proxima_dosis = str(fecha_proxima_dosis).strip()
        else:
            self._fecha_proxima_dosis = self._calcular_proxima_dosis()

    # --- MÉTODO AUXILIAR PARA CÁLCULO AUTOMÁTICO DE VENCIMIENTO ---
    def _calcular_proxima_dosis(self):
        fecha_app = datetime.strptime(self._fecha_aplicacion, "%Y-%m-%d")
        dias = self._vacuna.get_intervalo_dosis_dias()
        fecha_prox = fecha_app + timedelta(days=dias)
        return fecha_prox.strftime("%Y-%m-%d")

    # --- GETTERS ---
    def get_id_vacunacion(self):
        return self._id_vacunacion

    def get_vacuna(self):
        return self._vacuna

    def get_fecha_aplicacion(self):
        return self._fecha_aplicacion

    def get_fecha_proxima_dosis(self):
        return self._fecha_proxima_dosis

    # --- SETTERS CON VALIDACIÓN ---
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
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha de aplicación debe tener el formato válido AAAA-MM-DD.")
        self._fecha_aplicacion = fecha_str
        # Actualiza automáticamente la próxima dosis si cambia la fecha de aplicación
        self._fecha_proxima_dosis = self._calcular_proxima_dosis()

    def set_fecha_proxima_dosis(self, fecha_proxima_dosis):
        fecha_str = str(fecha_proxima_dosis).strip()
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha de próxima dosis debe tener el formato válido AAAA-MM-DD.")
        self._fecha_proxima_dosis = fecha_str

    def __str__(self):
        return (
            f"ID Registro: {self._id_vacunacion} | "
            f"Vacuna: {self._vacuna.get_nombre()} (Lote: {self._vacuna.get_lote()}) | "
            f"Aplicada: {self._fecha_aplicacion} | "
            f"Próxima dosis: {self._fecha_proxima_dosis}"
        )