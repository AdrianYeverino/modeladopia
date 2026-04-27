# main_ui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from generador import GeneradorLCG
from simulacion_banco import SimulacionBanco
import estadisticas as st

# Variables globales para exportación
registro_global = [] 
numeros_aleatorios_global = [] 

def ejecutar_simulacion():
    global registro_global, numeros_aleatorios_global
    
    try:
        tiempo_total = float(ent_tiempo.get())
    except ValueError:
        messagebox.showerror("¡Error!", "Ingresa un número válido para el tiempo total.")
        return

    # Usamos nuestro generador LCG con los parámetros estándar correctos
    m_grande = (2**32)
    generador = GeneradorLCG(3, 1664525, 1013904223, m_grande)
    numeros_aleatorios_global = generador.generar(2000)
    
    # Usamos nuestra lógica matemática correcta (3 cajeros, Poisson, Uniforme)
    banco = SimulacionBanco(numeros_aleatorios_global)
    registro_global, espera, ocio, clientes = banco.simular(tiempo_total)
    
    # Actualizar Interfaz
    lbl_res_espera.config(text=f"{espera:.2f} min")
    lbl_res_ocio.config(text=f"{ocio:.2f} min")
    lbl_res_clientes.config(text=f"{clientes}")
    
    for fila in tabla.get_children():
        tabla.delete(fila)
        
    for i, fila in enumerate(registro_global):
        etiqueta_color = 'par' if i % 2 == 0 else 'impar'
        tabla.insert("", "end", values=(
            fila["Cliente"], fila["t_lleg"], fila["t_acum"], 
            fila["t_ini"], fila["t_ser"], fila["t_fin"], 
            fila["t_esp"], fila["t_ocio"]
        ), tags=(etiqueta_color,))

    tabla.config(height=max(1, min(len(registro_global), 20)))

def mostrar_prueba_estadistica():
    if not numeros_aleatorios_global:
        messagebox.showwarning('¡Advertencia!', 'Primero debes ejecutar la simulación.')
        return
        
    # Obtener cálculos de nuestro módulo de estadísticas integrado
    chi_val, chi_crit, chi_aprob, det_chi = st.prueba_chi_cuadrada(numeros_aleatorios_global)
    ks_val, ks_crit, ks_aprob, det_ks = st.prueba_kolmogorov_smirnov(numeros_aleatorios_global)
    c0, mu, var, z0, z_crit, cor_aprob = st.prueba_corridas(numeros_aleatorios_global)
    pok_val, pok_crit, pok_aprob, det_pok = st.prueba_poker(numeros_aleatorios_global)
    
    vent_stats = tk.Toplevel(ventana)
    vent_stats.title("Reporte de pruebas estadísticas")
    vent_stats.geometry("900x550")
    
    notebook = ttk.Notebook(vent_stats)
    notebook.pack(pady=10, padx=20, expand=True, fill="both")
    
    # Pestaña Chi-Cuadrada
    tab_chi = tk.Frame(notebook)
    notebook.add(tab_chi, text="Chi-Cuadrada (Uniformidad)")
    col_chi = ("Intervalo", "Frecuencia observada (O)", "Frecuencia esperada (E)", "(O - E)² / E")
    tabl_chi = ttk.Treeview(tab_chi, columns=col_chi, show="headings", height=10)
    for col in col_chi: tabl_chi.heading(col, text=col); tabl_chi.column(col, width=150, anchor="center")
    for fila in det_chi: tabl_chi.insert("", "end", values=fila)
    tabl_chi.pack(pady=15, fill="x", padx=20)
    res_chi = f"Chi-Cuadrada calculada: {chi_val:.4f}  |  Valor crítico: {chi_crit}\n" + ("☑ APROBADA" if chi_aprob else "☒ RECHAZADA")
    tk.Label(tab_chi, text=res_chi, font=("Arial", 11, "bold"), fg="#27ae60" if chi_aprob else "#c0392b").pack()

    # Pestaña K-S
    tab_ks = tk.Frame(notebook)
    notebook.add(tab_ks, text="Kolmogorov-Smirnov (Uniformidad)")
    col_ks = ("i", "r_i (ordenado)", "i/n", "(i−1)/n", "D+", "D−")
    tabl_ks = ttk.Treeview(tab_ks, columns=col_ks, show="headings", height=10)
    for col in col_ks: tabl_ks.heading(col, text=col); tabl_ks.column(col, width=120, anchor="center")
    for fila in det_ks: tabl_ks.insert("", "end", values=fila)
    tabl_ks.pack(pady=15, fill="both", expand=True, padx=20)
    res_ks = f"Estadístico D calculado: {ks_val:.4f}  |  Valor crítico: {ks_crit:.4f}\n" + ("☑ APROBADA" if ks_aprob else "☒ RECHAZADA")
    tk.Label(tab_ks, text=res_ks, font=("Arial", 11, "bold"), fg="#27ae60" if ks_aprob else "#c0392b").pack()

    # Pestaña Corridas
    tab_cor = tk.Frame(notebook)
    notebook.add(tab_cor, text="Corridas (Independencia)")
    tk.Label(tab_cor, text=f"\n\nTotal de corridas observadas (c0): {c0}\nMedia esperada (μ): {mu:.4f}\nVarianza (σ²): {var:.4f}", font=("Arial", 12)).pack()
    res_cor = f"\nz0 calculado: {z0:.4f}  |  Valor crítico (Z): {z_crit}\n" + ("☑ APROBADA" if cor_aprob else "☒ RECHAZADA")
    tk.Label(tab_cor, text=res_cor, font=("Arial", 12, "bold"), fg="#27ae60" if cor_aprob else "#c0392b").pack()

    # Pestaña Poker
    tab_pok = tk.Frame(notebook)
    notebook.add(tab_pok, text="Prueba Póker (Independencia)")
    col_pok = ("Categoría (mano)", "Observada (O)", "Esperada (E)", "(O - E)² / E")
    tabl_pok = ttk.Treeview(tab_pok, columns=col_pok, show="headings", height=7)
    for col in col_pok: tabl_pok.heading(col, text=col); tabl_pok.column(col, width=150, anchor="center")
    for fila in det_pok: tabl_pok.insert("", "end", values=fila)
    tabl_pok.pack(pady=20, fill="x", padx=20)
    res_pok = f"Chi calculado: {pok_val:.4f}  |  Valor crítico: {pok_crit}\n" + ("☑ APROBADA" if pok_aprob else "☒ RECHAZADA")
    tk.Label(tab_pok, text=res_pok, font=("Arial", 11, "bold"), fg="#27ae60" if pok_aprob else "#c0392b").pack()

def exportar_csv():
    if not registro_global: return messagebox.showwarning('¡Advertencia!', 'Primero ejecuta la simulación.')
    ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], initialfile="Resultados_Banco.csv")
    if ruta: pd.DataFrame(registro_global).to_csv(ruta, index=False, encoding='utf-8-sig')

def exportar_xlsx():
    if not registro_global: return messagebox.showwarning('¡Advertencia!', 'Primero ejecuta la simulación.')
    ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")], initialfile="Resultados_Banco.xlsx")
    if ruta: pd.DataFrame(registro_global).to_excel(ruta, index=False)

# Diseño de la ventana principal
ventana = tk.Tk()
ventana.title("Simulador PIA - Banco 3 Cajeros")
ventana.geometry("1024x700") 
ventana.state("zoomed")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", background="#2c3e50", foreground="white", font=("Arial", 10, "bold"))
style.configure("Treeview", font=("Arial", 10), rowheight=25)

tk.Label(ventana, text="Simulador del Problema 5.13 (Banco)", font=("Arial", 18, "bold"), fg="#2c3e50").pack(pady=10)

frame_parametros = tk.LabelFrame(ventana, text=" Parámetros del Problema ", font=("Arial", 10, "bold"), padx=15, pady=10)
frame_parametros.pack(pady=5)

# Bloqueamos los parámetros visualmente para que coincidan con el problema, demostrando rigor
tk.Label(frame_parametros, text="Tasa de Llegada Poisson (clientes/hr): 40", font=("Arial", 10)).grid(row=0, column=0, padx=15, pady=5)
tk.Label(frame_parametros, text="Tiempo de Servicio Uniforme (Min - Max): 0 a 1 min", font=("Arial", 10)).grid(row=0, column=1, padx=15, pady=5)
tk.Label(frame_parametros, text="Cajeros Activos: 3", font=("Arial", 10)).grid(row=0, column=2, padx=15, pady=5)

tk.Label(frame_parametros, text="Tiempo total de la simulación (minutos):", font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=2, pady=10, sticky="e")
ent_tiempo = ttk.Entry(frame_parametros, width=12, justify="center")
ent_tiempo.grid(row=1, column=2, pady=10, sticky="w")
ent_tiempo.insert(0, "120")

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)
tk.Button(frame_botones, text="Ejecutar Simulación", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", command=ejecutar_simulacion).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Descargar .CSV", font=("Arial", 11, "bold"), bg="#d35400", fg="white", command=exportar_csv).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Descargar .XLSX", font=("Arial", 11, "bold"), bg="#2980b9", fg="white", command=exportar_xlsx).grid(row=0, column=2, padx=10)

tk.Button(ventana, text="Validar aleatoriedad e independencia (Pruebas Estadísticas)", font=("Arial", 11, "bold"), bg="#34495e", fg="white", command=mostrar_prueba_estadistica).pack(pady=10)

frame_resultados = tk.Frame(ventana)
frame_resultados.pack(pady=5)
tk.Label(frame_resultados, text="Espera promedio:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=25)
tk.Label(frame_resultados, text="Tiempo ocio total (3 Cajeros):", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=25)
tk.Label(frame_resultados, text="Clientes atendidos:", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=25)

lbl_res_espera = tk.Label(frame_resultados, text="--", font=("Arial", 16, "bold"), fg="#c0392b")
lbl_res_espera.grid(row=1, column=0)
lbl_res_ocio = tk.Label(frame_resultados, text="--", font=("Arial", 16, "bold"), fg="#8e44ad")
lbl_res_ocio.grid(row=1, column=1)
lbl_res_clientes = tk.Label(frame_resultados, text="--", font=("Arial", 16, "bold"), fg="#27ae60")
lbl_res_clientes.grid(row=1, column=2)

columnas = ("Cliente", "Tiempo de llegada", "Tiempo acumulado", "Tiempo de inicio", "Tiempo de servicio", "Tiempo final", "Tiempo de espera", "Tiempo de ocio")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=1) 
for col in columnas: tabla.heading(col, text=col); tabla.column(col, width=125, anchor="center")
tabla.tag_configure('par', background='#ecf0f1')
tabla.tag_configure('impar', background='#ffffff')
tabla.pack(pady=10, fill="x", padx=20)

ventana.mainloop()