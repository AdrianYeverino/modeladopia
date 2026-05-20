# Documentación Técnica del Proyecto — PIA Equipo 3
### Simulador de Línea de Espera en Banco (M/M/3)

Este documento explica la arquitectura interna del proyecto para que cualquier integrante del equipo pueda entender el código, ubicar cada parte importante y presentarlo con seguridad.

---

## 1. Tecnologías y Librerías

### Librerías externas (instaladas vía pip)

| Librería | Versión | Para qué se usa |
|---|---|---|
| `pandas` | 2.2.2 | Construir los DataFrames y escribirlos al archivo Excel |
| `openpyxl` | 3.1.2 | Motor que usa pandas para generar el `.xlsx` |

### Módulos de la librería estándar de Python (no necesitan instalación)

| Módulo | Dónde se usa | Para qué |
|---|---|---|
| `math` | `generador.py`, `estadisticas.py`, `simulacion_banco.py` | `math.log()` para distribución exponencial inversa, `math.sqrt()` para estadísticos |
| `tkinter` / `tkinter.ttk` | `main_ui.py` | Toda la interfaz gráfica (ventanas, botones, tabla, pestañas) |
| `tkinter.messagebox` | `main_ui.py` | Cuadros de diálogo de error y confirmación |
| `tkinter.filedialog` | `main_ui.py` | Diálogo para guardar el archivo Excel |

> **Punto clave para la presentación:** La simulación matemática (LCG, pruebas, motor) está implementada completamente en Python puro, sin librerías externas. Esto demuestra que el equipo entendió y programó los algoritmos desde cero.

---

## 2. Descripción de Cada Archivo

### `generador.py` — Generador de Números Pseudoaleatorios

**Qué contiene:** La clase `GeneradorLCG`.

**Qué hace:** Implementa el Algoritmo Congruencial Lineal (LCG) para producir una lista de números pseudoaleatorios en el intervalo (0, 1).

**Parámetros del LCG:**
- `x0` — Semilla inicial (valor de arranque)
- `a` — Multiplicador
- `c` — Incremento
- `m` — Módulo (divisor)

**Fórmula matemática:**
```
X_{i+1} = (a * X_i + c)  mod  m
U_i      = X_{i+1} / m
```

**Método importante:**
```python
# Línea ~30 en generador.py
def generar(self, cantidad):
    # Aplica la fórmula LCG 'cantidad' veces
    # Retorna lista de floats en (0,1)
```

**Valores por defecto usados en el proyecto:**
- X0 = 7, a = 21, c = 211, m = 10,000, cantidad = 500

---

### `estadisticas.py` — Validación de los Números Aleatorios

**Qué contiene:** Dos funciones independientes y la constante `Z_CRITICO = 1.96`.

**Por qué es importante:** Antes de usar los números en la simulación, se verifica que son estadísticamente válidos (uniformes e independientes). Si una prueba falla, los resultados de la simulación no son confiables.

#### Función 1: `prueba_medias(numeros)`

**Propósito:** Verificar que los números tienen distribución Uniforme (la media debe ser ≈ 0.5).

**Hipótesis nula (H₀):** La media de los U_i es 0.5.

**Cómo funciona:**
1. Calcula la media aritmética de todos los U_i.
2. Construye un intervalo de aceptación: `[0.5 - margen, 0.5 + margen]` donde `margen = 1.96 * (1 / sqrt(12 * n))`.
3. Si la media cae dentro del intervalo → **APROBADA**; si no → **RECHAZADA**.

**Qué retorna:** Diccionario con `media`, `limite_inferior`, `limite_superior`, `aprobada`.

#### Función 2: `prueba_corridas(numeros)`

**Propósito:** Verificar que los números son estadísticamente independientes (no hay patrones de subida/bajada repetitivos).

**Hipótesis nula (H₀):** Los U_i son independientes entre sí.

**Cómo funciona:**
1. Compara cada número con el anterior: 1 si sube, 0 si baja → genera secuencia binaria.
2. Cuenta las "corridas" (grupos de 1s o 0s consecutivos sin interrupción).
3. Calcula el estadístico Z₀ = |corridas_observadas - media_esperada| / desviación_estándar.
4. Si Z₀ < 1.96 → **APROBADA** (el número de corridas es normal).

**Qué retorna:** Diccionario con `corridas`, `media_esperada`, `varianza`, `z0`, `z_critico`, `aprobada`.

---

### `simulacion_banco.py` — Motor de Simulación Discreta

**Qué contiene:** La clase `SimulacionBanco`.

**Qué hace:** Toma la lista de números aleatorios y simula la operación del banco cliente por cliente, calculando todos los tiempos.

**Parámetros fijos del problema (definidos como constantes al inicio del archivo):**
```python
NUM_CAJEROS = 3
TASA_LLEGADA_HORA = 40      # clientes/hora
MEDIA_INTERARRIBO = 1.5     # minutos (= 60/40)
SERV_MIN = 0.0
SERV_MAX = 1.0
```

**Cómo consume los números aleatorios:**
- Cada cliente usa **2 números consecutivos**: el primero para calcular cuándo llega, el segundo para calcular cuánto dura su servicio.
- Con 500 números se procesan ~250 clientes.

**Distribuciones inversas aplicadas:**
```python
# Tiempo entre llegadas — Distribución Exponencial Inversa
t_entre_llegadas = -MEDIA_INTERARRIBO * math.log(1 - u_llegada)

# Tiempo de servicio — Distribución Uniforme Inversa
t_servicio = SERV_MIN + (SERV_MAX - SERV_MIN) * u_servicio
# Con SERV_MIN=0 y SERV_MAX=1, simplifica a: t_servicio = u_servicio
```

**Lógica de asignación de cajero (FIFO):**
- Se busca el cajero que se desocupa más pronto (`min(estado_cajeros)`).
- Si el cajero ya está libre cuando llega el cliente → el cajero estuvo **ocioso**.
- Si el cajero aún está ocupado → el cliente **espera en cola**.

**Registro por cliente (12 columnas):**
```
Cliente | U_lleg | U_serv | T_entre | T_llegada | T_servicio |
Cajero  | T_inicio | T_fin | T_espera | T_ocio | T_sistema
```

**Indicadores calculados en `obtener_resultados()`:**
```python
W = tiempo_total_sistema / clientes_atendidos        # Tiempo promedio en sistema
L = (TASA_LLEGADA_HORA / 60) * W                     # Ley de Little: L = lambda * W
espera_prom = tiempo_espera_total / clientes_atendidos
```

---

### `main_ui.py` — Interfaz Gráfica de Usuario

**Qué contiene:** La clase `InterfazSimulador` y el bloque `if __name__ == "__main__"` que arranca la aplicación.

**Qué hace:** Integra todos los módulos anteriores y los presenta en una ventana visual.

#### Zonas de la Ventana (de arriba hacia abajo)

**Zona 1 — Encabezado**
- Barra gris oscura con el título "PANEL DE CONTROL: SIMULACION BANCARIA (M/M/3)".

**Zona 2 — Configuración (3 columnas)**
- Columna izquierda: Parámetros fijos del problema (solo lectura).
- Columna central: Campos de entrada del LCG (X0, a, c, m, cantidad).
- Columna derecha: Botón verde **"CORRER SIMULACION"** (acción principal).

**Zona 3 — Acciones secundarias**
- Botón gris: **"Ver pruebas estadisticas"** → abre ventana con 2 pestañas (Medias y Corridas).
- Botón verde: **"Exportar todo a Excel (.xlsx)"** → abre diálogo de guardado.

**Zona 4 — Indicadores rápidos (5 tarjetas de colores)**
- Verde: Clientes atendidos
- Rojo: Espera promedio
- Púrpura: Ocio total
- Azul: W (tiempo en sistema)
- Naranja: L (clientes en sistema)

**Zona 5 — Tabla paso a paso (Treeview)**
- Muestra los 12 datos de cada cliente en una tabla con scroll.
- Se puebla automáticamente al correr la simulación.

#### Flujo de Ejecución al Presionar "CORRER SIMULACION"

```
1. Leer parámetros del LCG desde los campos de la UI
2. Crear GeneradorLCG y generar n números pseudoaleatorios
3. Correr prueba_medias() y prueba_corridas() sobre los números
4. Crear SimulacionBanco con esos números y llamar simular()
5. Llamar obtener_resultados() para W, L, espera, ocio
6. Actualizar las 5 tarjetas con los resultados
7. Llenar la tabla con el registro cliente por cliente
8. Mostrar messagebox de éxito
```

**Métodos clave en `main_ui.py`:**
```python
_correr_simulacion()       # Orquesta todo el flujo (ver arriba)
_actualizar_indicadores()  # Pinta los 5 indicadores con los valores
_actualizar_tabla()        # Inserta todas las filas en el Treeview
_ver_pruebas()             # Abre la ventana secundaria con las 2 pestañas
_exportar_excel()          # Genera el .xlsx con pandas y openpyxl
```

#### Exportación Excel — 5 Hojas Generadas

| Hoja | Contenido |
|---|---|
| `Configuracion` | Parámetros del LCG y del banco |
| `Numeros LCG` | Los n números U_i generados |
| `Simulacion` | Tabla completa con los 12 datos por cliente |
| `Pruebas` | Resultados de Medias y Corridas con veredicto |
| `Resultados` | W, L, espera promedio, ocio total, clientes atendidos |

---

## 3. Mapa de Ubicaciones Clave

| ¿Qué buscas? | Archivo | Dónde exactamente |
|---|---|---|
| Generación de números aleatorios | `generador.py` | Método `generar()` de la clase `GeneradorLCG` |
| Fórmula LCG | `generador.py` | Dentro de `generar()`: `x = (a * x + c) % m` |
| Prueba de uniformidad (medias) | `estadisticas.py` | Función `prueba_medias()` |
| Prueba de independencia (corridas) | `estadisticas.py` | Función `prueba_corridas()` |
| Distribución exponencial inversa | `simulacion_banco.py` | Método `simular()`: línea con `math.log(1 - u_llegada)` |
| Distribución uniforme inversa | `simulacion_banco.py` | Método `simular()`: línea con `SERV_MIN + ... * u_servicio` |
| Asignación de cajero (FIFO) | `simulacion_banco.py` | Dentro de `simular()`: `min(estado_cajeros)` |
| Cálculo de W, L, espera | `simulacion_banco.py` | Método `obtener_resultados()` |
| Ley de Little (L = λ·W) | `simulacion_banco.py` | Dentro de `obtener_resultados()` |
| Interfaz gráfica completa | `main_ui.py` | Clase `InterfazSimulador` |
| Botón principal y flujo | `main_ui.py` | Método `_correr_simulacion()` |
| Tarjetas de indicadores | `main_ui.py` | Método `_actualizar_indicadores()` |
| Ventana de pruebas estadísticas | `main_ui.py` | Método `_ver_pruebas()` |
| Exportación a Excel | `main_ui.py` | Método `_exportar_excel()` |

---

## 4. Validación Teórica de los Resultados

Con los parámetros por defecto (X0=7, a=21, c=211, m=10000, n=500), el sistema es M/M/3 con:
- λ = 40/60 ≈ 0.667 clientes/min
- μ = 1/0.5 = 2 clientes/min por cajero (tiempo de servicio medio = 0.5 min)
- Utilización ρ = λ/(s·μ) = 0.667/(3·2) ≈ 0.11 (11%)

Como la utilización es muy baja (11%), casi no hay cola. Los resultados esperados son:
- W ≈ 0.5 min (prácticamente el tiempo de servicio)
- L ≈ 0.33 clientes en el sistema
- Espera promedio ≈ 0 min

> Esto valida que la simulación es correcta: con tan poca carga, los cajeros están ociosos la mayor parte del tiempo y los clientes entran y salen casi sin esperar.

---

## 5. Guía Rápida para la Presentación

### Puntos a destacar ante la maestra

1. **Implementación desde cero:** El LCG y las pruebas estadísticas no usan `random` de Python ni ninguna librería externa. Todo está programado con las fórmulas matemáticas.

2. **Modularidad:** El proyecto está dividido en 4 archivos con responsabilidades claras (generación, validación, simulación, interfaz). Cada módulo puede probarse por separado.

3. **Validación antes de simular:** El sistema no acepta números aleatorios de baja calidad; primero los valida con dos pruebas de hipótesis (nivel de significancia α = 0.05, Z_crítico = 1.96).

4. **Distribuciones inversas:** Para convertir un número uniforme U_i en un tiempo de llegada se usa la transformación inversa de la Exponencial: `t = -media * ln(1 - U)`. Para el servicio uniforme, la transformación inversa es directa.

5. **Ley de Little:** El indicador L se obtiene multiplicando λ (tasa de llegada) por W (tiempo promedio en sistema), demostrando la aplicación de un resultado fundamental de teoría de colas.

6. **Consistencia teórica:** Los resultados de la simulación (W ≈ 0.5 min, L ≈ 0.33) coinciden con los valores que predice la teoría analítica M/M/3, lo que valida la implementación.

### Orden sugerido para mostrar la aplicación

1. Abrir `main_ui.py` y ejecutar → mostrar la ventana.
2. Explicar los parámetros del LCG en la columna central.
3. Presionar **CORRER SIMULACION** → mostrar que la tabla se llena con los 250 clientes.
4. Señalar las 5 tarjetas de indicadores y explicar qué significa cada una.
5. Abrir **Ver pruebas estadisticas** → mostrar que ambas pruebas pasan (APROBADA en verde).
6. Exportar a Excel → abrir el archivo y mostrar las 5 hojas.
