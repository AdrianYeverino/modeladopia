# Resumen de cambios del refactor

Documento de control con todas las modificaciones aplicadas al PIA
(Problema 5.13 - Simulacion Bancaria) desde la solicitud inicial de
"reducir pruebas y simplificar codigo" hasta el rediseno final con
tabla visible y exportacion a Excel.

---

## 1. Contexto

Las instrucciones de optimizacion vivian en `folder_md/`:

- `Contexto_PIA_Simulacion_Banco_version2.md` (marco teorico).
- `Prompt_Claude_Optimizacion_PIA.md` (diagnostico + reglas de refactor).

Los puntos clave del prompt fueron:

1. **Parametros del banco constantes** (3 cajeros, 40 clientes/hora,
   servicio Uniforme 0-1 min). La UI no debe permitir editarlos.
2. **Solo 2 pruebas estadisticas** (Medias + Corridas Arriba/Abajo)
   en lugar de las 4 originales (Chi-Cuadrada, K-S, Corridas, Poker).
3. **LCG con valores pequenios pero validos** (`X0=7, a=21, c=211,
   m=10000`) para que el grupo entienda los numeros en pantalla.
4. **Documentacion didactica en espaniol** explicando cada formula.

---

## 2. Iteracion 1 - Simplificacion inicial

### `generador.py`
- LCG reescrito con valores nuevos por defecto: `X0=7, a=21, c=211, m=10000`.
- Comentarios paso a paso explicando la formula `X_{i+1} = (a*X_i + c) mod m`
  y la normalizacion `U_i = X_{i+1} / m`.

### `estadisticas.py`
- Se eliminaron las pruebas de **Chi-Cuadrada**, **Kolmogorov-Smirnov**
  y **Poker**.
- Quedaron solo dos funciones:
  - `prueba_medias(numeros)` -> uniformidad (intervalo de aceptacion
    `0.5 +/- Z * 1/sqrt(12n)`).
  - `prueba_corridas(numeros)` -> independencia (conteo de rachas y
    estadistico `Z0 = |c0 - mu| / sigma`).
- Constante global `Z_CRITICO = 1.96` (alpha = 0.05).
- Cada bloque comentado con la formula correspondiente del material de clase.

### `simulacion_banco.py`
- Parametros del problema convertidos en constantes a nivel de modulo:
  `NUM_CAJEROS = 3`, `TASA_LLEGADA_HORA = 40`, `SERV_MIN = 0`,
  `SERV_MAX = 1`, `MEDIA_INTERARRIBO = 1.5`.
- Constructor simplificado: solo recibe la lista de numeros U_i.
- Calculo de W (tiempo en sistema) y L (clientes en sistema) aplicando
  la Ley de Little `L = lambda * W`.

### `main_ui.py` (primera version compacta)
- Ventana reducida a 400x300 px.
- Etiquetas fijas con los datos del problema (sin cajas de entrada).
- Un solo boton central `EJECUTAR SIMULACION`.
- Resultados en un `ScrolledText` con veredicto de las 2 pruebas y los
  valores de W, L.

### Archivos auxiliares
- Eliminado `simulacion.py` (codigo viejo no usado).
- Eliminado `__pycache__/` (basura de Python).
- `requirements.txt` vaciado (no se necesitaban dependencias externas).

---

## 3. Iteracion 2 - Rediseno final (UI visible + Excel)

Despues de la primera iteracion, la UI quedo demasiado pequeña y se
perdio la tabla con el paso a paso y la exportacion a Excel. Se rehizo:

### `simulacion_banco.py`
- Se anadieron acumuladores adicionales:
  `tiempo_espera_total` y `tiempo_ocio_total`.
- El registro por cliente ahora contiene 12 columnas:
  `Cliente, U_lleg, U_serv, T_entre, T_llegada, T_servicio, Cajero,
  T_inicio, T_fin, T_espera, T_ocio, T_sistema`.
- `obtener_resultados()` regresa un diccionario con W, L, espera
  promedio, ocio total y total de clientes atendidos.

### `main_ui.py`
- Ventana de **1100x720** con cinco zonas:
  1. Encabezado con titulo.
  2. Tres bloques de parametros:
     - Datos fijos del problema (etiquetas no editables).
     - LCG configurable (X0, a, c, m, cantidad de numeros).
     - Boton grande de ejecucion.
  3. Barra de acciones (ver pruebas / exportar Excel).
  4. **Cinco indicadores** en tarjetas: Atendidos, Espera promedio,
     Ocio total, W, L.
  5. **Tabla `Treeview`** con scroll que muestra una fila por cliente.
- Ventana secundaria con `Notebook` de **2 pestañas** (Medias y
  Corridas), cada una con valores observados, limites de aceptacion
  y veredicto coloreado.

### Exportacion a Excel (multi-hoja)
El boton **Exportar todo a Excel (.xlsx)** genera un libro con
cinco hojas:

| Hoja            | Contenido                                              |
|-----------------|--------------------------------------------------------|
| `Configuracion` | Parametros del LCG y del problema 5.13                 |
| `Numeros LCG`   | Los U_i generados (i, U_i)                             |
| `Simulacion`    | Paso a paso con las 12 columnas del registro           |
| `Pruebas`       | Veredictos de medias y corridas                        |
| `Resultados`    | W, L, espera promedio, ocio total, clientes atendidos  |

### `requirements.txt`
- Restaurados `pandas==2.2.2` y `openpyxl==3.1.2` para soportar el
  Excel multi-hoja.

---

## 4. Resultados de la simulacion (validacion)

Corriendo `main_ui.py` con la configuracion por defecto
(`X0=7, a=21, c=211, m=10000`, 500 numeros U_i):

```
Clientes atendidos     : 250
Espera promedio        : 0.000 min   (cola practicamente vacia)
Ocio total             : 845.36 min  (utilizacion ~11%)
W (tiempo en sistema)  : 0.508 min
L (clientes en sistema): 0.339 clientes
```

Pruebas estadisticas:

```
[Medias]   media = 0.4803   limites = [0.4747, 0.5253]   APROBADA
[Corridas] c0 = 318   mu = 333   Z0 = 1.594 < 1.96       APROBADA
```

Los valores son coherentes con la teoria M/M/3:
- Tasa lambda = 40/h = 0.667/min.
- Tiempo medio de servicio = 0.5 min  ->  mu = 2/min.
- Utilizacion rho = lambda / (s*mu) = 0.667 / (3*2) ~ 0.11.
- Por la utilizacion tan baja casi no hay espera, asi que W ~ 0.5 min
  (igual al tiempo medio de servicio) y L ~ lambda * W ~ 0.34.

---

## 5. Estructura final del proyecto

```
modeladopia/
|-- generador.py          (LCG con parametros pequenios)
|-- estadisticas.py       (Medias + Corridas)
|-- simulacion_banco.py   (Motor M/M/3 con registro detallado)
|-- main_ui.py            (UI 1100x720 con tabla y export)
|-- requirements.txt      (pandas + openpyxl)
|-- README.md
|-- CAMBIOS.md            (este documento)
`-- folder_md/
    |-- Contexto_PIA_Simulacion_Banco_version2.md
    `-- Prompt_Claude_Optimizacion_PIA.md
```

---

## 6. Como ejecutar

```powershell
# 1) Activar entorno virtual (PowerShell en Windows).
.\.venv\Scripts\Activate.ps1

# 2) (Solo la primera vez) instalar dependencias.
pip install -r requirements.txt

# 3) Lanzar la interfaz.
python main_ui.py
```

Al pulsar **CORRER SIMULACION** se muestran los indicadores y la
tabla con el paso a paso. **Ver pruebas estadisticas** abre la ventana
con las dos pestañas y **Exportar todo a Excel** guarda un archivo
con las cinco hojas listas para entregar.
