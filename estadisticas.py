# estadisticas.py
import math

# Pruebas de uniformidad
def prueba_chi_cuadrada(numeros, intervalos=10):
    n = len(numeros)
    frecuencia_esperada = n / intervalos
    frecuencia_observada = [0] * intervalos
    
    for r in numeros:
        indice = int(r * intervalos) 
        if indice == intervalos: 
            indice -= 1
        frecuencia_observada[indice] += 1 
        
    detalles = []
    chi_cuadrada_calculada = 0
    
    for i in range(intervalos):
        rango = f"{i/intervalos:.1f} - {(i+1)/intervalos:.1f}"
        o = frecuencia_observada[i] 
        e = frecuencia_esperada 
        calculo = ((o - e)**2) / e 
        chi_cuadrada_calculada += calculo
        detalles.append((rango, o, e, round(calculo, 4)))
    
    limite_critico = 16.919
    prueba = chi_cuadrada_calculada < limite_critico
    return chi_cuadrada_calculada, limite_critico, prueba, detalles

def prueba_kolmogorov_smirnov(numeros):
    n = len(numeros)    
    numeros_ordenados = sorted(numeros) 
    detalles_ks = []
    d_mas_max = 0
    d_menos_max = 0
    
    for i in range(n):
        r_i = numeros_ordenados[i]
        i_mas_1 = i + 1
        d_mas_i = (i_mas_1 / n) - r_i 
        d_menos_i = r_i - (i / n)
        
        if d_mas_i > d_mas_max: d_mas_max = d_mas_i 
        if d_menos_i > d_menos_max: d_menos_max = d_menos_i 
        
        detalles_ks.append((
            i_mas_1, round(r_i, 5), round(i_mas_1 / n, 5), 
            round(i / n, 5), round(d_mas_i, 5), round(d_menos_i, 5)
        ))
        
    d_calculado = max(d_mas_max, d_menos_max)
    d_critico = 1.36 / math.sqrt(n)
    prueba = d_calculado < d_critico
    return d_calculado, d_critico, prueba, detalles_ks

# Pruebas de independencia
def prueba_corridas(numeros):
    n = len(numeros)
    secuencia = []
    for i in range(1, n):
        if numeros[i] > numeros[i-1]: secuencia.append(1)
        else: secuencia.append(0)
            
    c0 = 1
    for i in range(1, len(secuencia)):
        if secuencia[i] != secuencia[i-1]: c0 += 1
            
    mu = (2 * n - 1) / 3
    varianza = (16 * n - 29) / 90
    sigma = math.sqrt(varianza)
    z0 = abs((c0 - mu) / sigma)
    z_critico = 1.96
    prueba = z0 < z_critico
    return c0, mu, varianza, z0, z_critico, prueba

def prueba_poker(numeros):
    n = len(numeros)
    categorias = {"TD": 0, "1P": 0, "2P": 0, "T": 0, "TP": 0, "P": 0, "Q": 0}
    probabilidades = {"TD": 0.30240, "1P": 0.50400, "2P": 0.10800, "T": 0.07200, "TP": 0.00900, "P": 0.00450, "Q": 0.00010}
    
    for r in numeros:
        str_r = str(r).split('.')
        if len(str_r) > 1:
            decimales = str_r[1][:5].ljust(5, '0')
        else:
            decimales = "00000"
            
        conteos = {}
        for digito in decimales: conteos[digito] = conteos.get(digito, 0) + 1
        valores = list(conteos.values())
        valores.sort(reverse=True)
        
        if valores == [1, 1, 1, 1, 1]: cat = "TD"
        elif valores == [2, 1, 1, 1]: cat = "1P"
        elif valores == [2, 2, 1]: cat = "2P"
        elif valores == [3, 1, 1]: cat = "T"
        elif valores == [3, 2]: cat = "TP"
        elif valores == [4, 1]: cat = "P"
        elif valores == [5]: cat = "Q"
        
        categorias[cat] += 1

    chi_cuadrada_calculada = 0
    detalles_poker = []
    for cat in categorias:
        o = categorias[cat]
        e = n * probabilidades[cat]
        calculo = ((o - e)**2) / e if e > 0 else 0
        chi_cuadrada_calculada += calculo
        detalles_poker.append((cat, o, round(e, 4), round(calculo, 4)))
        
    limite_critico = 12.592
    prueba = chi_cuadrada_calculada < limite_critico
    return chi_cuadrada_calculada, limite_critico, prueba, detalles_poker