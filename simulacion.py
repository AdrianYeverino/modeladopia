# simulacion_banco.py
# Módulo que contiene la lógica del sistema dinámico del banco.

import math

class SimulacionBanco:
    """
    Modelo discreto, estocástico y dinámico de una línea de espera en un banco.
    """
    def __init__(self, numeros_aleatorios):
        # Componentes del modelo
        self.num_cajeros = 3
        # Variables de estado: Tiempo en el que cada cajero se desocupa
        self.estado_cajeros = [0.0] * self.num_cajeros 
        
        # Exógenas: Tasa de llegadas Poisson de 40 clientes/hora.
        # Esto significa que el tiempo entre llegadas (interarribo) es Exponencial
        # Media = 60 minutos / 40 clientes = 1.5 minutos entre cliente y cliente.
        self.media_interarribo = 1.5 
        
        # Se requieren 2 números aleatorios por cliente (1 para llegada, 1 para servicio)
        self.numeros_aleatorios = numeros_aleatorios
        
        # Variables Endógenas (Resultados)
        self.tiempo_total_sistema = 0.0
        self.clientes_atendidos = 0
        self.tiempo_fin_simulacion = 0.0

    def simular(self):
        """
        Ejecuta la simulación de eventos discretos.
        """
        tiempo_reloj = 0.0
        
        # Procesamos clientes mientras haya pares de números aleatorios suficientes
        for i in range(0, len(self.numeros_aleatorios) - 1, 2):
            u_llegada = self.numeros_aleatorios[i]
            u_servicio = self.numeros_aleatorios[i+1]
            
            # 1. Generar tiempo entre llegadas (Distribución Exponencial inversa)
            # T_a = -media * ln(1 - U)
            tiempo_entre_llegadas = -self.media_interarribo * math.log(1 - u_llegada)
            
            # Avanzar el reloj de simulación al momento de la llegada del cliente
            tiempo_reloj += tiempo_entre_llegadas
            tiempo_llegada_cliente = tiempo_reloj
            
            # 2. Generar tiempo de servicio (Distribución Uniforme 0 a 1 minuto)
            # T_s = a + (b - a) * U -> 0 + (1 - 0) * U = U
            tiempo_servicio = u_servicio
            
            # 3. Determinar qué cajero atenderá al cliente
            # La disciplina de cola es FIFO. El cliente va al cajero que se desocupe primero.
            cajero_asignado = self.estado_cajeros.index(min(self.estado_cajeros))
            tiempo_disponible_cajero = self.estado_cajeros[cajero_asignado]
            
            # El cliente comienza a ser atendido cuando llega o cuando el cajero se libera
            tiempo_inicio_servicio = max(tiempo_llegada_cliente, tiempo_disponible_cajero)
            
            # 4. Calcular el fin del servicio y actualizar el estado del cajero
            tiempo_fin_servicio = tiempo_inicio_servicio + tiempo_servicio
            self.estado_cajeros[cajero_asignado] = tiempo_fin_servicio
            
            # 5. Calcular variables endógenas (tiempo en el sistema)
            tiempo_en_sistema_cliente = tiempo_fin_servicio - tiempo_llegada_cliente
            self.tiempo_total_sistema += tiempo_en_sistema_cliente
            self.clientes_atendidos += 1
            
            # Guardar el último momento de la simulación
            if tiempo_fin_servicio > self.tiempo_fin_simulacion:
                self.tiempo_fin_simulacion = tiempo_fin_servicio
                
    def obtener_resultados(self):
        """
        Calcula y retorna W (Tiempo promedio) y L (Cantidad promedio de clientes).
        """
        if self.clientes_atendidos == 0:
            return 0, 0
            
        # W = Suma de tiempos en el sistema / Número de clientes
        w_promedio = self.tiempo_total_sistema / self.clientes_atendidos
        
        # L = λ * W (Ley de Little). 
        # Tasa de llegada λ = 40 por hora = 40/60 por minuto = 0.6667
        lambda_minuto = 40 / 60
        l_promedio = lambda_minuto * w_promedio
        
        return w_promedio, l_promedio