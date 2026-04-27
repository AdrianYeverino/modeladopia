import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from generador import GeneradorLCG
from simulacion_banco import SimulacionBanco
import estadisticas as st

class InterfazProfesional:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistemas Dinámicos - PIA Equipo 3")
        self.root.geometry("1150x800")
        self.root.configure(bg="#eceff1")
        
        # Variables de almacenamiento de datos
        self.registro_data = []
        self.numeros_gen = []

        self.setup_ui()

    def setup_ui(self):
        # --- Encabezado ---
        header = tk.Frame(self.root, bg="#263238", height=70)
        header.pack(fill="x")
        tk.Label(header, text="PANEL DE CONTROL: SIMULACIÓN BANCARIA (M/M/s)", 
                 font=("Segoe UI", 16, "bold"), fg="white", bg="#263238").pack(pady=20)

        # --- Contenedor Principal de Parámetros ---
        params_container = tk.Frame(self.root, bg="#eceff1", padx=20, pady=10)
        params_container.pack(fill="x")

        # 1. Bloque LCG (Generador de Números)
        lcg_frame = tk.LabelFrame(params_container, text=" Configuración del Generador (LCG) ", 
                                  font=("Segoe UI", 9, "bold"), bg="white", padx=10, pady=10)
        lcg_frame.grid(row=0, column=0, padx=10, sticky="nsew")
        
        self.val_x0 = self.create_input(lcg_frame, "Semilla (X0):", "3", 0)
        self.val_a = self.create_input(lcg_frame, "Multiplicador (a):", "1664525", 1)
        self.val_c = self.create_input(lcg_frame, "Incremento (c):", "1013904223", 2)
        self.val_m = self.create_input(lcg_frame, "Módulo (m):", "4294967296", 3)

        # 2. Bloque del Sistema (Variables Exógenas)
        bank_frame = tk.LabelFrame(params_container, text=" Parámetros del Sistema (Banco) ", 
                                   font=("Segoe UI", 9, "bold"), bg="white", padx=10, pady=10)
        bank_frame.grid(row=0, column=1, padx=10, sticky="nsew")

        self.val_llegada = self.create_input(bank_frame, "Llegadas (Clientes/Hr):", "40", 0)
        self.val_cajeros = self.create_input(bank_frame, "Número de Cajeros:", "3", 1)
        self.val_serv_min = self.create_input(bank_frame, "Servicio Min (min):", "0.0", 2)
        self.val_serv_max = self.create_input(bank_frame, "Servicio Max (min):", "1.0", 3)

        # 3. Bloque de Simulación y Ejecución
        sim_frame = tk.LabelFrame(params_container, text=" Ejecución ", 
                                  font=("Segoe UI", 9, "bold"), bg="white", padx=10, pady=10)
        sim_frame.grid(row=0, column=2, padx=10, sticky="nsew")
        
        self.val_tiempo = self.create_input(sim_frame, "Duración (min):", "120", 0)
        
        btn_run = tk.Button(sim_frame, text="CORRER SIMULACIÓN", bg="#1b5e20", fg="white", 
                            font=("Segoe UI", 10, "bold"), command=self.ejecutar, height=2)
        btn_run.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # --- Área de Resultados (Indicadores y Tabla) ---
        self.setup_results_area()

    def create_input(self, parent, label, default, row):
        tk.Label(parent, text=label, bg="white", font=("Segoe UI", 8)).grid(row=row, column=0, padx=5, pady=2, sticky="e")
        entry = ttk.Entry(parent, width=18, justify="center")
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    def setup_results_area(self):
        # Botones de Acción Secundaria
        actions_bar = tk.Frame(self.root, bg="#eceff1")
        actions_bar.pack(pady=10)
        
        tk.Button(actions_bar, text="Ver Reporte de Pruebas Estadísticas", bg="#37474f", fg="white", 
                  font=("Segoe UI", 9, "bold"), command=self.abrir_pruebas).grid(row=0, column=0, padx=10)
        
        tk.Button(actions_bar, text="Descargar Excel (.xlsx)", bg="#2e7d32", fg="white", 
                  font=("Segoe UI", 9), command=self.exportar_excel).grid(row=0, column=1, padx=10)

        # Panel de Indicadores Rápidos
        stats_panel = tk.Frame(self.root, bg="#eceff1")
        stats_panel.pack(fill="x", padx=40)
        
        self.lbl_espera = self.create_stat_label(stats_panel, "Espera Promedio", "#c62828", 0)
        self.lbl_ocio = self.create_stat_label(stats_panel, "Ocio Total", "#4527a0", 1)
        self.lbl_atendidos = self.create_stat_label(stats_panel, "Clientes Atendidos", "#2e7d32", 2)

        # Tabla de Datos (Eventos Discretos)
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=25, pady=15)
        
        columns = ("Cliente", "T. Llegada", "T. Acumulado", "T. Inicio", "T. Servicio", "T. Fin", "T. Espera", "T. Ocio")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def create_stat_label(self, parent, text, color, col):
        frame = tk.Frame(parent, bg="white", relief="flat", bd=1, padx=20, pady=5)
        frame.grid(row=0, column=col, padx=20, pady=10, sticky="ew")
        parent.columnconfigure(col, weight=1)
        
        tk.Label(frame, text=text, bg="white", font=("Segoe UI", 9)).pack()
        label_val = tk.Label(frame, text="--", bg="white", font=("Segoe UI", 14, "bold"), fg=color)
        label_val.pack()
        return label_val

    def ejecutar(self):
        try:
            # 1. Generar Números Aleatorios
            gen = GeneradorLCG(
                int(self.val_x0.get()), 
                int(self.val_a.get()), 
                int(self.val_c.get()), 
                int(self.val_m.get())
            )
            # Generamos suficientes números (2 por cliente potencial)
            self.numeros_gen = gen.generar(5000) 
            
            # 2. Configurar y Correr Simulación
            banco = SimulacionBanco(
                self.numeros_gen, 
                int(self.val_cajeros.get()), 
                float(self.val_llegada.get()), 
                float(self.val_serv_min.get()), 
                float(self.val_serv_max.get())
            )
            
            self.registro_data, espera, ocio, atendidos = banco.simular(float(self.val_tiempo.get()))
            
            # 3. Actualizar UI
            self.lbl_espera.config(text=f"{espera:.2f} min")
            self.lbl_ocio.config(text=f"{ocio:.2f} min")
            self.lbl_atendidos.config(text=f"{atendidos}")
            
            for item in self.tree.get_children(): self.tree.delete(item)
            for row in self.registro_data:
                self.tree.insert("", "end", values=list(row.values()))
            
            messagebox.showinfo("Éxito", "Simulación finalizada correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error de Parámetros", f"Verifique que todos los campos sean numéricos.\n{e}")

    def abrir_pruebas(self):
        if not self.numeros_gen:
            messagebox.showwarning("Atención", "Debe ejecutar la simulación primero para validar los números generados.")
            return

        # Obtener resultados matemáticos del archivo estadisticas.py
        chi_val, chi_crit, chi_aprob, det_chi = st.prueba_chi_cuadrada(self.numeros_gen)
        ks_val, ks_crit, ks_aprob, det_ks = st.prueba_kolmogorov_smirnov(self.numeros_gen)
        c0, mu, var, z0, z_crit, cor_aprob = st.prueba_corridas(self.numeros_gen)
        pok_val, pok_crit, pok_aprob, det_pok = st.prueba_poker(self.numeros_gen)

        # Crear ventana de reporte
        vent_stats = tk.Toplevel(self.root)
        vent_stats.title("Reporte de Validación Estadística (Aleatoriedad)")
        vent_stats.geometry("950x600")
        vent_stats.configure(bg="#f5f5f5")

        notebook = ttk.Notebook(vent_stats)
        notebook.pack(pady=10, padx=20, expand=True, fill="both")

        # Pestaña Chi-Cuadrada
        tab_chi = tk.Frame(notebook, bg="white")
        notebook.add(tab_chi, text="Chi-Cuadrada")
        self.create_table_in_tab(tab_chi, ("Intervalo", "O", "E", "(O-E)²/E"), det_chi, 
                                 f"Calculado: {chi_val:.4f} | Crítico: {chi_crit}", chi_aprob)

        # Pestaña K-S
        tab_ks = tk.Frame(notebook, bg="white")
        notebook.add(tab_ks, text="Kolmogorov-Smirnov")
        self.create_table_in_tab(tab_ks, ("i", "ri", "i/n", "(i-1)/n", "D+", "D-"), det_ks, 
                                 f"D Máximo: {ks_val:.4f} | D Crítico: {ks_crit:.4f}", ks_aprob)

        # Pestaña Corridas
        tab_cor = tk.Frame(notebook, bg="white")
        notebook.add(tab_cor, text="Prueba de Corridas")
        tk.Label(tab_cor, text=f"\nCorridas (c0): {c0}\nMedia: {mu:.2f}\nVarianza: {var:.4f}", bg="white", font=("Segoe UI", 11)).pack()
        res_txt = f"Z0: {z0:.4f} | Z Crítico: {z_crit}\n" + ("☑ PASÓ PRUEBA" if cor_aprob else "☒ FALLÓ PRUEBA")
        tk.Label(tab_cor, text=res_txt, font=("Segoe UI", 12, "bold"), bg="white", fg="#2e7d32" if cor_aprob else "#c62828").pack(pady=20)

        # Pestaña Póker
        tab_pok = tk.Frame(notebook, bg="white")
        notebook.add(tab_pok, text="Prueba de Póker")
        self.create_table_in_tab(tab_pok, ("Mano", "O", "E", "Cálculo"), det_pok, 
                                 f"Chi Calculado: {pok_val:.4f} | Crítico: {pok_crit}", pok_aprob)

    def create_table_in_tab(self, parent, cols, data, footer_text, aprob):
        t = ttk.Treeview(parent, columns=cols, show="headings", height=8)
        for c in cols: 
            t.heading(c, text=c)
            t.column(c, width=140, anchor="center")
        for f in data: t.insert("", "end", values=f)
        t.pack(pady=10, padx=10, fill="x")
        
        status = "☑ APROBADA" if aprob else "☒ RECHAZADA"
        tk.Label(parent, text=f"{footer_text}\n{status}", font=("Segoe UI", 11, "bold"), 
                 bg="white", fg="#2e7d32" if aprob else "#c62828").pack(pady=5)

    def exportar_excel(self):
        if not self.registro_data:
            messagebox.showwarning("Error", "No hay datos para exportar. Ejecute la simulación.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if path:
            pd.DataFrame(self.registro_data).to_excel(path, index=False)
            messagebox.showinfo("Guardado", "Archivo exportado con éxito.")

if __name__ == "__main__":
    root = tk.Tk()
    # Aplicar un estilo global más moderno
    style = ttk.Style()
    style.theme_use("clam")
    app = InterfazProfesional(root)
    root.mainloop()