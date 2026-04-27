# Simulador de Sistemas Dinámicos: Línea de Espera en Banco 🏦

Este proyecto es el **Producto Integrador de Aprendizaje (PIA)** para la unidad de aprendizaje de *Modelado y Simulación de Sistemas Dinámicos*. Consiste en un simulador estocástico y discreto (orientado a eventos) desarrollado en Python con interfaz gráfica de usuario (GUI).

## 📖 Contexto del Proyecto (Problema 5.13)

El software resuelve analítica y computacionalmente el siguiente problema de teoría de colas (M/M/s):

> *"Un banco emplea 3 cajeros para servir a sus clientes. Los clientes arriban de acuerdo a un proceso Poisson a una razón de media de 40 por hora. Si un cliente encuentra todos los cajeros ocupados, entonces se incorpora a la cola que alimenta a todos los cajeros. El tiempo que dura la transacción entre un cajero y un cliente sigue una distribución uniforme entre 0 y 1 minuto."*

**Objetivos de la Simulación:**
1. Determinar el **tiempo promedio en el sistema** (W).
2. Determinar la **cantidad promedio de clientes en el sistema** (L).

## ✨ Características del Software

* **Generador LCG:** Implementación matemática del Algoritmo Congruencial Lineal para la generación de números pseudoaleatorios.
* **Validación Estadística:** Módulo integrado que evalúa la calidad de los números generados mediante pruebas de Uniformidad (Chi-Cuadrada, Kolmogorov-Smirnov) e Independencia (Corridas, Póker).
* **Motor de Simulación Discreta:** Algoritmo que procesa eventos paso a paso, gestionando el estado de los servidores (cajeros), los tiempos de llegada y tiempos de servicio.
* **Interfaz Gráfica (UI):** Entorno visual interactivo construido con `Tkinter` que permite parametrizar las variables exógenas del sistema y visualizar los resultados en tiempo real.
* **Exportación de Datos:** Capacidad de exportar el registro detallado de eventos discretos a archivos Excel (`.xlsx`) y `.csv`.

## 🗂️ Estructura del Proyecto

El proyecto está diseñado bajo una arquitectura modular separando la lógica matemática de la interfaz visual:

* `generador.py`: Contiene la clase `GeneradorLCG` con las variables de semilla, multiplicador, incremento y módulo.
* `estadisticas.py`: Funciones matemáticas para el cálculo de los valores observados y esperados, así como estadísticos críticos.
* `simulacion_banco.py`: Núcleo dinámico de la simulación. Recibe los aleatorios y aplica las distribuciones inversas (Exponencial y Uniforme).
* `main_ui.py`: Archivo principal. Despliega la interfaz gráfica, agrupa los módulos y maneja las interacciones del usuario.
* `requirements.txt`: Lista de dependencias externas.

## 🚀 Requisitos e Instalación

Para ejecutar este simulador, necesitas tener instalado **Python 3.8 o superior**.

### Paso 1: Instalar dependencias
Abre tu terminal o consola de comandos en la carpeta raíz del proyecto y ejecuta el siguiente comando para instalar las librerías necesarias para la manipulación de datos y exportación:

```bash
pip install -r requirements.txt