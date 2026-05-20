# =============================================================================
# estadisticas.py
# -----------------------------------------------------------------------------
# Modulo que contiene las DOS pruebas estadisticas seleccionadas (las mas
# sencillas del material de clase) para validar los numeros pseudoaleatorios
# generados por el LCG antes de usarlos en la simulacion.
#
# 1) Prueba de Medias    -> Valida UNIFORMIDAD  (Presentacion 7).
# 2) Prueba de Corridas  -> Valida INDEPENDENCIA (Presentacion 8).
#
# Ambas usan un nivel de significancia estandar alpha = 0.05 y un valor
# critico de Z = 1.96 tomado de la tabla normal estandar.
# =============================================================================

import math

# Valor critico Z para alpha = 0.05 (dos colas), tomado de la tabla normal.
Z_CRITICO = 1.96


# -----------------------------------------------------------------------------
# PRUEBA 1: PRUEBA DE MEDIAS  (Uniformidad)
# -----------------------------------------------------------------------------
# Hipotesis nula H0: la media de los U_i es 0.5 (estan distribuidos uniformemente).
#
# Si los numeros son verdaderamente uniformes en (0,1), su media muestral debe
# acercarse a 0.5. Calculamos un intervalo de aceptacion alrededor de 0.5:
#
#     limite_inferior = 0.5 - Z * (1 / sqrt(12 * n))
#     limite_superior = 0.5 + Z * (1 / sqrt(12 * n))
#
# Donde 1/12 es la varianza teorica de una distribucion uniforme (0,1).
# Si la media calculada cae dentro del intervalo => se APRUEBA H0.
# -----------------------------------------------------------------------------
def prueba_medias(numeros):
    n = len(numeros)

    # Media aritmetica de la muestra.
    media = sum(numeros) / n

    # Calculo de los limites de aceptacion usando Z = 1.96.
    margen = Z_CRITICO * (1 / math.sqrt(12 * n))
    limite_inferior = 0.5 - margen
    limite_superior = 0.5 + margen

    # Veredicto: la prueba se aprueba si la media cae dentro del intervalo.
    aprobada = limite_inferior <= media <= limite_superior

    return {
        "media": media,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "aprobada": aprobada,
    }


# -----------------------------------------------------------------------------
# PRUEBA 2: PRUEBA DE CORRIDAS ARRIBA Y ABAJO  (Independencia)
# -----------------------------------------------------------------------------
# Hipotesis nula H0: los numeros son independientes entre si.
#
# Pasos:
#  1) Construir una secuencia binaria comparando cada U_i con el anterior:
#       1 si U_i > U_{i-1}  (sube)
#       0 si U_i <= U_{i-1} (baja)
#  2) Contar el numero total de corridas (c0): cada vez que la secuencia
#     cambia de 0 a 1 o de 1 a 0 inicia una corrida nueva.
#  3) Comparar c0 con el numero esperado de corridas para una secuencia
#     verdaderamente aleatoria:
#         mu       = (2*n - 1) / 3
#         varianza = (16*n - 29) / 90
#         Z0       = |c0 - mu| / sqrt(varianza)
#  4) Si Z0 < 1.96 => se APRUEBA H0 (numeros independientes).
# -----------------------------------------------------------------------------
def prueba_corridas(numeros):
    n = len(numeros)

    # Paso 1: Construir secuencia de subidas (1) y bajadas (0).
    secuencia = []
    for i in range(1, n):
        if numeros[i] > numeros[i - 1]:
            secuencia.append(1)
        else:
            secuencia.append(0)

    # Paso 2: Contar el numero total de corridas observadas (c0).
    # Toda secuencia tiene al menos 1 corrida; se suma cada cambio de signo.
    c0 = 1
    for i in range(1, len(secuencia)):
        if secuencia[i] != secuencia[i - 1]:
            c0 += 1

    # Paso 3: Calcular la media y varianza teoricas de las corridas.
    mu = (2 * n - 1) / 3
    varianza = (16 * n - 29) / 90
    sigma = math.sqrt(varianza)

    # Estadistico Z0 (en valor absoluto, prueba de dos colas).
    z0 = abs((c0 - mu) / sigma)

    # Paso 4: Veredicto.
    aprobada = z0 < Z_CRITICO

    return {
        "corridas": c0,
        "media_esperada": mu,
        "varianza": varianza,
        "z0": z0,
        "z_critico": Z_CRITICO,
        "aprobada": aprobada,
    }
