# generador.py
# Módulo para la generación de números pseudoaleatorios.

class GeneradorLCG:
    """
    Clase que implementa el Algoritmo Congruencial Lineal (LCG).
    Fórmula: X_{i+1} = (a * X_i + c) mod m
    """
    def __init__(self, semilla, a, c, m):
        # Parámetros del modelo matemático
        self.semilla = semilla
        self.a = a
        self.c = c
        self.m = m

    def generar(self, cantidad):
        """
        Genera una lista de números pseudoaleatorios (U_i) entre 0 y 1.
        """
        numeros_aleatorios = []
        x_actual = self.semilla
        
        for _ in range(cantidad):
            # Aplicación de la fórmula congruencial lineal
            x_siguiente = (self.a * x_actual + self.c) % self.m
            
            # Normalización para obtener un número entre 0 y 1 (U_i)
            u_i = x_siguiente / self.m
            numeros_aleatorios.append(u_i)
            
            # Actualizar el estado para la siguiente iteración
            x_actual = x_siguiente
            
        return numeros_aleatorios