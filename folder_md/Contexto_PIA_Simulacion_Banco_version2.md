# Documentación Contextual y Requerimientos del Proyecto
**Producto Integrador de Aprendizaje (PIA) - Modelado y Simulación de Sistemas Dinámicos**

Este documento recopila todo el contexto, marco teórico, decisiones arquitectónicas y matemáticas aplicadas hasta la fecha para la resolución del problema planteado. Su propósito es servir como documentación oficial del equipo y como contexto estructurado ("prompt") para asistentes de Inteligencia Artificial que colaboren en la refinación del código.

---

## 1. Planteamiento del Problema (Problema 5.13)
"Un banco emplea 3 cajeros para servir a sus clientes. Los clientes arriban de acuerdo a un proceso de Poisson a una razón de media de 40 por hora. Si un cliente encuentra todos los cajeros ocupados, entonces se incorpora a la cola que alimenta a todos los cajeros. El tiempo que dura la transacción entre un cajero y un cliente sigue una distribución uniforme entre 0 y 1 minuto. Para esta información, ¿cuál es el tiempo promedio en el sistema?, ¿cuál es la cantidad promedio de clientes en el sistema?"

---

## 2. Definición y Clasificación del Modelo
De acuerdo con la teoría de sistemas dinámicos (Presentación 4), el modelo se clasifica estrictamente como:
* **Dinámico:** Las variables de estado (clientes en cola, cajeros ocupados) cambian a lo largo del tiempo.
* **Estocástico (Probabilístico):** Existen variables aleatorias en el proceso (llegadas y tiempos de servicio).
* **Discreto:** Los cambios de estado ocurren en momentos específicos en el tiempo (llegada de cliente, inicio de servicio, fin de servicio), impulsando una simulación orientada a eventos.
* **Simbólico/Matemático:** Representado a través de relaciones lógico-matemáticas programadas en código.

---

## 3. Elementos del Modelo (Teoría de Sistemas - Presentación 5)
* **Componentes:** Clientes, Línea de espera (Cola FIFO), 3 Cajeros (Servidores).
* **Variables Exógenas (De entrada):** * Tasa de llegadas ($\lambda$) = 40 clientes/hora (Proceso Poisson). 
  * Tiempo de servicio = Distribución Uniforme (Min: 0, Max: 1 minuto).
* **Variables de Estado:** Tiempo disponible de cada cajero (estado de ocupación), tiempo actual del reloj de simulación, cantidad de clientes en espera.
* **Variables Endógenas (Resultados buscados):**
  * $W$: Tiempo promedio que un cliente pasa en el sistema (Espera + Servicio).
  * $L$: Cantidad promedio de clientes en el sistema (Calculado posteriormente mediante la Ley de Little: $L = \lambda 	imes W$).
* **Restricciones/Parámetros:** Capacidad de servidores = 3. Disciplina = Primero en llegar, primero en ser atendido (FIFO).

---

## 4. Generación de Números Aleatorios
Para simular las variables exógenas (llegadas y servicios) se requiere una fuente robusta de números aleatorios $U_i \sim U(0,1)$.
* **Método Seleccionado:** Algoritmo Congruencial Lineal (LCG).
* **Justificación:** Es el estándar recomendado en la Presentación 6 para obtener un periodo máximo de vida ($N = m$) antes de repetirse, previniendo sesgos en simulaciones de larga duración.
* **Parámetros Matemáticos Rigurosos (Basados en *Numerical Recipes*):**
  * Semilla ($X_0$): 3 (configurable)
  * Multiplicador ($a$): 1664525
  * Incremento ($c$): 1013904223
  * Módulo ($m$): $2^{32}$ (4294967296)

---

## 5. Pruebas Estadísticas Aplicadas
No se asume la calidad del LCG; se valida matemáticamente antes de la simulación. Basado en las Presentaciones 7 y 8, los números generados deben cumplir con dos propiedades fundamentales: **Uniformidad** e **Independencia**.

**Pruebas de Uniformidad:** (Para garantizar que los números cubren el rango $[0,1]$ de forma pareja y su media tiende a 0.5 con varianza de 1/12).
1. **Prueba Chi-Cuadrada:** Compara la frecuencia observada en 10 intervalos contra la frecuencia esperada.
2. **Prueba de Kolmogorov-Smirnov (K-S):** Evalúa la diferencia máxima absoluta entre la distribución acumulada empírica y la teórica.

**Pruebas de Independencia:** (Para garantizar que un número no influye o predice la aparición del siguiente).
3. **Prueba de Corridas (Arriba y Abajo):** Evalúa la secuencia de crecimiento o decrecimiento de los números (buscando tendencias o patrones ocultos).
4. **Prueba de Póker:** Clasifica grupos de 5 decimales en "manos de póker" (todos diferentes, un par, dos pares, tercia, etc.) y contrasta las frecuencias observadas con las probabilidades teóricas.

*Nota técnica:* Solo si los números aprueban estas validaciones ($lpha = 0.05$), se transforman en tiempos reales de simulación (Exponencial inversa para Poisson y Uniforme $a+(b-a)U$ para el servicio).

---

## 6. Arquitectura de Software Requerida
El proyecto exige un diseño modular que separe la lógica de interfaz (UI) de las matemáticas puras. 

* **generador.py:** Módulo que aloja la clase del Generador LCG.
* **estadisticas.py:** Módulo funcional que contiene los cálculos críticos de las 4 pruebas estadísticas, devolviendo estadísticos calculados, valores críticos de la tabla y veredictos booleanos (Aprobado/Rechazado).
* **simulacion_banco.py:** Módulo principal de la lógica orientada a eventos. Transforma los números $U_i$ en horas/minutos, administra la fila de 3 cajeros y calcula los acumuladores para $W$ y $L$.
* **main_ui.py:** Script de interfaz gráfica nativa construido con `tkinter`. 
  * Requerimientos de UI: Debe permitir parametrizar tanto el sistema bancario como el generador, mostrar indicadores rápidos, desplegar una tabla tipo datagrid con el registro de clientes, una ventana en pestañas (Notebook) para los resultados de las 4 pruebas, y poseer botones de exportación.
* **Dependencias Externas (`requirements.txt`):** `pandas` y `openpyxl` (Exclusivamente para exportación de registros a Excel/CSV).
