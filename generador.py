# =============================================================================
# generador.py
# -----------------------------------------------------------------------------
# Modulo encargado de generar numeros pseudoaleatorios U_i en el intervalo (0,1)
# mediante el Algoritmo Congruencial Lineal (LCG) visto en la Presentacion 6.
#
# Formula matematica:
#     X_{i+1} = (a * X_i + c) mod m
#     U_i    = X_{i+1} / m
#
# Donde:
#     X_0 = Semilla inicial
#     a   = Multiplicador
#     c   = Incremento
#     m   = Modulo (define el periodo maximo del generador)
# =============================================================================


class GeneradorLCG:
    """
    Generador Congruencial Lineal con parametros pequenios y legibles
    para facilitar la explicacion en clase.
    """

    def __init__(self, semilla=7, a=21, c=211, m=10000):
        # Se usan valores pequenios pero validos matematicamente para evitar
        # ciclos inmediatos y a la vez mantener numeros faciles de leer.
        self.semilla = semilla
        self.a = a
        self.c = c
        self.m = m

    def generar(self, cantidad):
        """
        Genera una lista con 'cantidad' numeros U_i pseudoaleatorios.
        Cada U_i se obtiene normalizando X_{i+1} entre m, asi U_i pertenece a (0,1).
        """
        numeros = []
        x_actual = self.semilla

        for _ in range(cantidad):
            # Paso 1: Aplicar la formula congruencial lineal.
            x_siguiente = (self.a * x_actual + self.c) % self.m

            # Paso 2: Normalizar el entero al intervalo (0,1) dividiendo entre m.
            u_i = x_siguiente / self.m
            numeros.append(u_i)

            # Paso 3: Actualizar el estado para la siguiente iteracion.
            x_actual = x_siguiente

        return numeros
