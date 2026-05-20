# Simulador de Sistemas Dinámicos: Línea de Espera en Banco

Este proyecto es el **Producto Integrador de Aprendizaje (PIA)** para la unidad de aprendizaje de *Modelado y Simulación de Sistemas Dinámicos*. Consiste en un simulador estocástico discreto (orientado a eventos) desarrollado en Python con interfaz gráfica de usuario (GUI) construida con Tkinter.

---

## Contexto del Proyecto (Problema 5.13)

El software resuelve el siguiente problema clásico de teoría de colas (M/M/s):

> *"Un banco emplea 3 cajeros para servir a sus clientes. Los clientes arriban de acuerdo a un proceso Poisson a una razón de media de 40 por hora. Si un cliente encuentra todos los cajeros ocupados, entonces se incorpora a la cola que alimenta a todos los cajeros. El tiempo que dura la transacción entre un cajero y un cliente sigue una distribución uniforme entre 0 y 1 minuto."*

**Objetivos de la simulación:**
1. Determinar el **tiempo promedio en el sistema** (W).
2. Determinar la **cantidad promedio de clientes en el sistema** (L) mediante la Ley de Little.

---

## Características del Software

- **Generador LCG:** Implementación del Algoritmo Congruencial Lineal (LCG) para generar números pseudoaleatorios configurables por el usuario (semilla, multiplicador, incremento, módulo).
- **Validación Estadística:** Dos pruebas de hipótesis que validan la calidad de los números generados: Prueba de Medias (uniformidad) y Prueba de Corridas (independencia).
- **Motor de Simulación Discreta:** Algoritmo paso a paso que gestiona llegadas, asignación de cajeros y tiempos de servicio aplicando distribuciones inversas (Exponencial para llegadas, Uniforme para servicio).
- **Interfaz Gráfica (UI):** Panel de control construido con Tkinter/ttk que permite parametrizar el LCG, ejecutar la simulación y visualizar los resultados en una tabla de 12 columnas.
- **Exportación a Excel:** Genera un archivo `.xlsx` con 5 hojas: Configuracion, Numeros LCG, Simulacion, Pruebas y Resultados.

---

## Estructura del Proyecto

```
modeladopia/
├── generador.py          # Clase GeneradorLCG: algoritmo LCG
├── estadisticas.py       # Prueba de Medias y Prueba de Corridas
├── simulacion_banco.py   # Motor de simulación discreta (M/M/3)
├── main_ui.py            # Interfaz gráfica principal (Tkinter)
└── requirements.txt      # Dependencias externas (pandas, openpyxl)
```

---

## Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.8+ | Lenguaje base |
| Tkinter / ttk | Interfaz gráfica de usuario |
| pandas 2.2.2 | Exportación de datos a Excel |
| openpyxl 3.1.2 | Motor de escritura de archivos .xlsx |
| math (stdlib) | Cálculos matemáticos (log, sqrt) |

> La simulación en sí no depende de librerías externas: el LCG, las pruebas estadísticas y el motor de simulación están implementados desde cero en Python puro.

---

## Requisitos e Instalación

Necesitas **Python 3.8 o superior** instalado.

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
python main_ui.py
```

---

## Uso

1. Al abrir la aplicación, los parámetros del LCG tienen valores predeterminados (X0=7, a=21, c=211, m=10000, n=500).
2. Presiona **CORRER SIMULACION** para generar los números, validarlos y ejecutar la simulación.
3. La tabla muestra el paso a paso de cada cliente (hasta ~250 con 500 números).
4. Usa **Ver pruebas estadisticas** para revisar los resultados de Medias y Corridas.
5. Usa **Exportar todo a Excel** para guardar todos los datos en un archivo `.xlsx`.

---

## Parámetros Fijos del Sistema (Problema 5.13)

| Parámetro | Valor |
|---|---|
| Cajeros (servidores) | 3 |
| Tasa de llegada (lambda) | 40 clientes/hora |
| Media entre llegadas | 1.5 minutos |
| Distribución de servicio | Uniforme [0, 1] minutos |

---

## Indicadores Calculados

| Indicador | Descripción | Fórmula |
|---|---|---|
| W | Tiempo promedio en el sistema | W = suma(T_sistema) / atendidos |
| L | Clientes promedio en el sistema | L = lambda * W (Ley de Little) |
| Espera promedio | Tiempo promedio en cola | suma(T_espera) / atendidos |
| Ocio total | Minutos acumulados sin atender | suma(T_ocio) por los 3 cajeros |

---

## Equipo

PIA Equipo 3 — Modelado y Simulación de Sistemas Dinámicos, Sexto Semestre.
