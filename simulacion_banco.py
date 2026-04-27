# simulacion_banco.py
import math

class SimulacionBanco:
    """
    Modelo discreto, estocástico y dinámico de una línea de espera en un banco
    con 3 cajeros, llegadas Poisson y servicio Uniforme.
    """
    def __init__(self, numeros_aleatorios):
        self.num_cajeros = 3
        # Rastrea en qué minuto se desocupa cada uno de los 3 cajeros
        self.estado_cajeros = [0.0] * self.num_cajeros 
        
        # 40 clientes/hora = 1.5 minutos entre cliente y cliente en promedio
        self.media_interarribo = 1.5 
        self.numeros_aleatorios = numeros_aleatorios
        
        self.tiempo_espera_total = 0.0
        self.tiempo_ocio_total = 0.0
        self.clientes_atendidos = 0
        self.registro = [] # Aquí guardaremos los datos para la tabla UI

    def simular(self, tiempo_total_simulacion=120):
        tiempo_reloj = 0.0
        
        # Iteramos tomando de 2 en 2 (uno para llegada, otro para servicio)
        for i in range(0, len(self.numeros_aleatorios) - 1, 2):
            u_llegada = self.numeros_aleatorios[i]
            u_servicio = self.numeros_aleatorios[i+1]
            
            # 1. Proceso Poisson: Tiempo entre llegadas (Exponencial inversa)
            t_llegada = -self.media_interarribo * math.log(1 - u_llegada)
            tiempo_reloj += t_llegada
            t_acum = tiempo_reloj
            
            if t_acum > tiempo_total_simulacion:
                break # Termina la simulación si rebasamos el tiempo límite
                
            # 2. Tiempo de servicio (Uniforme 0 a 1 minuto)
            t_servicio = u_servicio
            
            # 3. Disciplina FIFO con 3 cajeros
            # Encontramos el cajero que se desocupa más pronto
            cajero_asignado = self.estado_cajeros.index(min(self.estado_cajeros))
            tiempo_disponible = self.estado_cajeros[cajero_asignado]
            
            # 4. Cálculo de tiempos de inicio, espera y ocio
            if t_acum >= tiempo_disponible:
                t_ini = t_acum
                t_ocio = t_ini - tiempo_disponible
                self.tiempo_ocio_total += t_ocio
                t_esp = 0.0
            else:
                t_ini = tiempo_disponible
                t_esp = t_ini - t_acum
                self.tiempo_espera_total += t_esp
                t_ocio = 0.0
                
            t_fin = t_ini + t_servicio
            self.estado_cajeros[cajero_asignado] = t_fin
            self.clientes_atendidos += 1
            
            # 5. Guardar registro para la Interfaz Gráfica
            self.registro.append({
                "Cliente": self.clientes_atendidos,
                "t_lleg": round(t_llegada, 2),
                "t_acum": round(t_acum, 2),
                "t_ini": round(t_ini, 2),
                "t_ser": round(t_servicio, 2),
                "t_fin": round(t_fin, 2),
                "t_esp": round(t_esp, 2),
                "t_ocio": round(t_ocio, 2)
            })

        espera_promedio = self.tiempo_espera_total / self.clientes_atendidos if self.clientes_atendidos > 0 else 0
        return self.registro, espera_promedio, self.tiempo_ocio_total, self.clientes_atendidos