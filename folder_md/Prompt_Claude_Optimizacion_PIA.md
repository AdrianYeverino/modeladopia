# Contexto y Directrices para la Optimización del Código de Simulación (Problema 5.13)

Este documento contiene las especificaciones detalladas, el diagnóstico de problemas actuales y los requerimientos de reducción de código para reestructurar el software del Producto Integrador de Aprendizaje (PIA). El objetivo es proporcionarle este archivo a un asistente de Inteligencia Artificial (como Claude) para delimitar el desarrollo a una versión compacta, pedagógica y de rápido entendimiento para la exposición en clase.

---

## 1. Definición del Problema Real (Problema 5.13)
"Un banco emplea 3 cajeros para servir a sus clientes. Los clientes arriban de acuerdo a un proceso de Poisson a una razón de media de 40 por hora. Si un cliente encuentra todos los cajeros ocupados, entonces se incorpora a la cola que alimenta a todos los cajeros. El tiempo que dura la transacción entre un cajero y un cliente sigue una distribución uniforme entre 0 y 1 minuto. Para esta información, ¿cuál es el tiempo promedio en el sistema?, ¿cuál es la cantidad promedio de clientes en el sistema?"

---

## 2. Diagnóstico de Dificultades y Errores Detectados
En las revisiones previas del proyecto se identificaron tres fallas críticas que afectan la calificación académica y la claridad del código:

1. **Incongruencia Conceptual en la Interfaz (UI):** Las versiones anteriores permitían al usuario modificar el número de cajeros, las tasas de llegada y los rangos de servicio. Esto abre la posibilidad de errores de captura durante la presentación y contradice las condiciones fijas del Problema 5.13.
2. **Saturación y Complejidad Estadística:** Se estaban aplicando cuatro pruebas estadísticas avanzadas (Chi-Cuadrada, Kolmogorov-Smirnov, Corridas y Póker). Esto generaba un código gigante, difícil de explicar para el equipo y con una curva de aprendizaje excesivamente alta para la audiencia de la clase.
3. **Periodos de Generación Incorrectos:** El uso de módulos numéricos extremadamente pequeños generaba ciclos repetitivos inmediatos, lo que provocaba el rechazo automático de las pruebas de aleatoriedad. Se requiere un balance entre un número comprensible para los estudiantes y la validez matemática.

---

## 3. Decisiones de Optimización y Reducción

### A. Congelación de Parámetros del Sistema
Las variables del banco se deben codificar de manera fija y constante dentro del motor de simulación. La interfaz de usuario no debe solicitar entradas para estos parámetros, garantizando que el simulador siempre arroje las respuestas correctas para el problema planteado:
* Servidores (Cajeros activos) = 3 constantes.
* Tasa de llegada Poisson = 40 clientes/hora (Tiempo de interarribo promedio de 1.5 minutos mediante la transformada inversa exponencial: `-media * ln(1 - U)`).
* Tiempo de servicio = Distribución Uniforme entre 0 y 1 minuto (Equivalente directo al número aleatorio generado: `t_servicio = U`).

### B. Selección de las 2 Pruebas Estadísticas Más Sencillas
Para reducir el tamaño del programa y asegurar una explicación fluida, el código se limitará estrictamente a dos pruebas (una de uniformidad y una de independencia) extraídas del material de clase (Presentaciones 7 y 8):

1. **Prueba de Medias (Validación de Uniformidad):** Es la más accesible debido a su lógica directa. Si los números pseudoaleatorios generados están distribuidos uniformemente entre 0 y 1, su promedio aritmético debe aproximarse a 0.5. El programa debe calcular la media de la muestra y verificar si se encuentra dentro de los límites normales de aceptación usando un nivel de significancia estandarizado ($lpha = 0.05$, $Z = 1.96$).
2. **Prueba de Corridas Arriba y Abajo (Validación de Independencia):** Es significativamente más sencilla de comprender que la prueba de Póker. Consiste en analizar la secuencia de números para determinar si el valor siguiente sube (1) o baja (0) respecto al anterior. Posteriormente se cuenta cuántas rachas o corridas se presentan en total. Si el número de rachas se asemeja al valor estadístico esperado por el azar, se aprueba la hipótesis de independencia.

### C. Simplificación del Generador LCG
Para evitar el uso de cifras excesivamente largas que confundan al grupo durante la lectura del código, se implementará el Algoritmo Congruencial Lineal ($X_{i+1} = (aX_i + c) \mod m$) utilizando valores enteros pequeños pero matemáticamente válidos para asegurar un periodo completo sin repeticiones inmediatas:
* Módulo ($m$) = 10,000 (Diez mil, una escala fácilmente legible).
* Multiplicador ($a$) = 21.
* Incremento ($c$) = 211.
* Semilla ($X_0$) = 7.

---

## 4. Instrucciones de Programación para el Asistente de IA (Prompt para Claude)

Actúa como un ingeniero de software experto en simulación estocástica y reescribe el proyecto bajo los siguientes criterios estrictos:

1. **Estructura Compacta y Limpia:** Une la lógica en archivos altamente legibles o en un único script modular bien seccionado, eliminando cualquier función, librería o código sobrante. El programa debe ser lo más corto posible sin perder rigor matemático.
2. **Diseño de Interfaz Enfocado:** Diseña una interfaz gráfica con Tkinter que sea compacta (máximo 400x300 píxeles). No debe incluir cajas de texto para ingresar cajeros o tasas de llegada; debe mostrar etiquetas fijas con los datos del Problema 5.13 y un único botón central para ejecutar el proceso completo.
3. **Resultados Directos:** Al presionar el botón, el programa debe mostrar en un cuadro de diálogo (`messagebox`) o panel de texto los resultados explícitos ordenados en dos bloques claros: el veredicto de las 2 pruebas estadísticas (Medias y Corridas con sus respectivos valores calculados y límites) y las respuestas finales a las preguntas del problema (Tiempo promedio en el sistema $W$ y cantidad promedio de clientes $L$ aplicando la Ley de Little).
4. **Documentación Didáctica:** Cada bloque del código debe estar minuciosamente comentado en español, explicando qué fórmula de las presentaciones de clase se está aplicando (Transformada inversa, límites de aceptación y conteo de rachas) para que cualquier estudiante sin experiencia previa en programación pueda explicarlo línea por línea frente al profesor.
