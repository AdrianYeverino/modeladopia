import math

class SimulacionBanco:
    def __init__(self, numeros_aleatorios, num_cajeros, tasa_llegada_hora, serv_min, serv_max):
        self.num_cajeros = num_cajeros
        self.estado_cajeros = [0.0] * self.num_cajeros 
        
        # λ = tasa_llegada_hora / 60 (clientes por minuto)
        # Media de interarribo = 1 / λ
        self.media_interarribo = 60.0 / tasa_llegada_hora 
        self.serv_min = serv_min
        self.serv_max = serv_max
        self.numeros_aleatorios = numeros_aleatorios
        
        self.tiempo_espera_total = 0.0
        self.tiempo_ocio_total = 0.0
        self.clientes_atendidos = 0
        self.registro = []

    def simular(self, tiempo_total_simulacion):
        tiempo_reloj = 0.0
        for i in range(0, len(self.numeros_aleatorios) - 1, 2):
            u_llegada = self.numeros_aleatorios[i]
            u_servicio = self.numeros_aleatorios[i+1]
            
            # Proceso Poisson (Exponencial inversa) 
            t_llegada = -self.media_interarribo * math.log(1 - u_llegada)
            tiempo_reloj += t_llegada
            t_acum = tiempo_reloj
            
            if t_acum > tiempo_total_simulacion:
                break
                
            # Tiempo de servicio Uniforme 
            t_servicio = self.serv_min + (self.serv_max - self.serv_min) * u_servicio
            
            cajero_asignado = self.estado_cajeros.index(min(self.estado_cajeros))
            tiempo_disponible = self.estado_cajeros[cajero_asignado]
            
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