# =============================================================================
# simulacion_banco.py
# -----------------------------------------------------------------------------
# Motor de simulacion por eventos discretos del Problema 5.13:
#   "Un banco emplea 3 cajeros... llegadas Poisson de 40 clientes/hora,
#    tiempo de servicio Uniforme entre 0 y 1 minuto."
#
# Por requerimiento del PIA, los parametros del sistema son CONSTANTES
# (no se piden por interfaz) para garantizar el escenario exacto del problema.
#
# Cada paso del proceso queda guardado en self.registro para que pueda
# visualizarse en la tabla de la UI y exportarse a Excel.
# =============================================================================

import math

# ----- Parametros FIJOS del problema 5.13 -----------------------------------
NUM_CAJEROS = 3                          # Servidores constantes.
TASA_LLEGADA_HORA = 40                   # Clientes por hora (lambda).
MEDIA_INTERARRIBO = 60.0 / TASA_LLEGADA_HORA  # 1.5 minutos entre clientes.
SERV_MIN = 0.0                           # Limite inferior del servicio (min).
SERV_MAX = 1.0                           # Limite superior del servicio (min).
# ----------------------------------------------------------------------------


class SimulacionBanco:
    """
    Modelo dinamico, estocastico y discreto del sistema de colas M/M/3.
    Calcula W (tiempo promedio en sistema) y L (clientes promedio en sistema)
    usando los numeros pseudoaleatorios U_i recibidos.
    """

    def __init__(self, numeros_aleatorios):
        # Variables de estado: tiempo en el que cada cajero queda libre.
        self.estado_cajeros = [0.0] * NUM_CAJEROS
        self.numeros = numeros_aleatorios

        # Acumuladores para resultados finales.
        self.tiempo_total_sistema = 0.0
        self.tiempo_espera_total = 0.0
        self.tiempo_ocio_total = 0.0
        self.clientes_atendidos = 0

        # Registro paso a paso (una fila por cliente). Se usa para la tabla
        # de la UI y para la hoja "Simulacion" del Excel.
        self.registro = []

    def simular(self):
        """
        Recorre los numeros aleatorios en pares (uno para llegada y otro
        para servicio) y va construyendo el reloj de simulacion.
        """
        tiempo_reloj = 0.0

        # Procesamos pares (U_llegada, U_servicio) -> un cliente por par.
        for i in range(0, len(self.numeros) - 1, 2):
            u_llegada = self.numeros[i]
            u_servicio = self.numeros[i + 1]

            # ----- 1) Tiempo entre llegadas: Exponencial inversa -----
            # Formula: T_a = -media * ln(1 - U)   (Presentacion 6).
            t_entre_llegadas = -MEDIA_INTERARRIBO * math.log(1 - u_llegada)
            tiempo_reloj += t_entre_llegadas
            t_llegada = tiempo_reloj

            # ----- 2) Tiempo de servicio: Uniforme (0,1) -----
            # Formula: T_s = a + (b - a)*U  ->  con a=0, b=1: T_s = U.
            t_servicio = SERV_MIN + (SERV_MAX - SERV_MIN) * u_servicio

            # ----- 3) Asignacion de cajero (FIFO) -----
            # El cliente entra con el cajero que se desocupe primero.
            cajero = self.estado_cajeros.index(min(self.estado_cajeros))
            disponible = self.estado_cajeros[cajero]

            # Si el cliente llega antes que el cajero termine -> espera.
            # Si el cliente llega despues -> el cajero estuvo ocioso ese rato.
            if t_llegada >= disponible:
                t_inicio = t_llegada
                t_espera = 0.0
                t_ocio = t_llegada - disponible
            else:
                t_inicio = disponible
                t_espera = disponible - t_llegada
                t_ocio = 0.0

            t_fin = t_inicio + t_servicio

            # Actualizamos el estado del cajero asignado.
            self.estado_cajeros[cajero] = t_fin

            # ----- 4) Acumular metricas -----
            t_en_sistema = t_fin - t_llegada
            self.tiempo_total_sistema += t_en_sistema
            self.tiempo_espera_total += t_espera
            self.tiempo_ocio_total += t_ocio
            self.clientes_atendidos += 1

            # Registro detallado por cliente. Cada columna se ve en la UI
            # y se exporta a la hoja "Simulacion" del Excel.
            self.registro.append({
                "Cliente": self.clientes_atendidos,
                "U_lleg": round(u_llegada, 4),
                "U_serv": round(u_servicio, 4),
                "T_entre": round(t_entre_llegadas, 3),
                "T_llegada": round(t_llegada, 3),
                "T_servicio": round(t_servicio, 3),
                "Cajero": cajero + 1,
                "T_inicio": round(t_inicio, 3),
                "T_fin": round(t_fin, 3),
                "T_espera": round(t_espera, 3),
                "T_ocio": round(t_ocio, 3),
                "T_sistema": round(t_en_sistema, 3),
            })

    def obtener_resultados(self):
        """
        Devuelve un diccionario con los indicadores principales.
        Todos los tiempos estan en minutos.
        """
        if self.clientes_atendidos == 0:
            return {"W": 0, "L": 0, "espera_prom": 0,
                    "ocio_total": 0, "atendidos": 0}

        # W = promedio de tiempos en el sistema (espera + servicio).
        w = self.tiempo_total_sistema / self.clientes_atendidos

        # Lambda en clientes por minuto.
        lambda_min = TASA_LLEGADA_HORA / 60.0

        # L = lambda * W   (Ley de Little).
        l = lambda_min * w

        # Espera promedio por cliente (solo cola, sin contar servicio).
        espera_prom = self.tiempo_espera_total / self.clientes_atendidos

        return {
            "W": w,
            "L": l,
            "espera_prom": espera_prom,
            "ocio_total": self.tiempo_ocio_total,
            "atendidos": self.clientes_atendidos,
        }
