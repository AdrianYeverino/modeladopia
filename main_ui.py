# =============================================================================
# main_ui.py
# -----------------------------------------------------------------------------
# Interfaz grafica del PIA - Simulacion Bancaria (Problema 5.13).
#
# La ventana muestra cuatro zonas claras:
#   1) Encabezado con titulo del proyecto.
#   2) Datos fijos del problema y configuracion del LCG.
#   3) Panel de indicadores (Espera, Ocio, Atendidos, W, L).
#   4) Tabla con el paso a paso de la simulacion (un renglon por cliente).
#
# Tambien hay dos botones secundarios:
#   * Ver pruebas estadisticas (Notebook con Medias y Corridas).
#   * Exportar todo a un archivo Excel con varias hojas.
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

from generador import GeneradorLCG
from simulacion_banco import (
    SimulacionBanco,
    NUM_CAJEROS, TASA_LLEGADA_HORA, SERV_MIN, SERV_MAX, MEDIA_INTERARRIBO,
)
import estadisticas as st


# Cantidad de numeros pseudoaleatorios que se generaran. Cada cliente consume
# 2 numeros (llegada y servicio); con 500 alcanzan para ~250 clientes.
CANTIDAD_NUMEROS = 500


class InterfazSimulador:
    """Ventana principal de la aplicacion."""

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistemas Dinamicos - PIA Equipo 3")
        self.root.geometry("1100x720")
        self.root.configure(bg="#eceff1")

        # Estado: datos generados por la ultima ejecucion.
        self.numeros = []
        self.registro = []
        self.resultado_medias = None
        self.resultado_corridas = None
        self.resultados = None

        self._construir_ui()

    # ==================================================================
    # Construccion de cada zona de la UI
    # ==================================================================
    def _construir_ui(self):
        self._zona_encabezado()
        self._zona_parametros()
        self._zona_acciones()
        self._zona_indicadores()
        self._zona_tabla()

    # --- 1) Encabezado --------------------------------------------------
    def _zona_encabezado(self):
        header = tk.Frame(self.root, bg="#263238", height=60)
        header.pack(fill="x")
        tk.Label(
            header,
            text="PANEL DE CONTROL: SIMULACION BANCARIA (M/M/3)",
            font=("Segoe UI", 15, "bold"), fg="white", bg="#263238",
        ).pack(pady=15)

    # --- 2) Parametros del problema + LCG -------------------------------
    def _zona_parametros(self):
        cont = tk.Frame(self.root, bg="#eceff1", padx=20, pady=10)
        cont.pack(fill="x")

        # 2a) Parametros FIJOS del problema (no se editan: son los datos
        #     exactos del Problema 5.13). Se muestran como etiquetas.
        f_banco = tk.LabelFrame(
            cont, text=" Datos fijos del Problema 5.13 ",
            font=("Segoe UI", 9, "bold"), bg="white", padx=15, pady=10,
        )
        f_banco.grid(row=0, column=0, padx=10, sticky="nsew")

        info = [
            ("Cajeros activos", f"{NUM_CAJEROS}"),
            ("Tasa de llegada (lambda)", f"{TASA_LLEGADA_HORA} clientes/hora"),
            ("Media interarribo", f"{MEDIA_INTERARRIBO:.2f} min"),
            ("Servicio (Uniforme)", f"[{SERV_MIN}, {SERV_MAX}] min"),
        ]
        for i, (k, v) in enumerate(info):
            tk.Label(f_banco, text=k + ":", bg="white",
                     font=("Segoe UI", 9)).grid(row=i, column=0, sticky="e", pady=2)
            tk.Label(f_banco, text=v, bg="white", fg="#1b5e20",
                     font=("Segoe UI", 9, "bold")).grid(
                         row=i, column=1, sticky="w", padx=8, pady=2)

        # 2b) Parametros del LCG. Si quedan vacios se usan los del problema.
        f_lcg = tk.LabelFrame(
            cont, text=" Generador LCG (configurable) ",
            font=("Segoe UI", 9, "bold"), bg="white", padx=15, pady=10,
        )
        f_lcg.grid(row=0, column=1, padx=10, sticky="nsew")

        self.val_x0 = self._input(f_lcg, "Semilla (X0):", "7", 0)
        self.val_a = self._input(f_lcg, "Multiplicador (a):", "21", 1)
        self.val_c = self._input(f_lcg, "Incremento (c):", "211", 2)
        self.val_m = self._input(f_lcg, "Modulo (m):", "10000", 3)
        self.val_n = self._input(f_lcg, "Cantidad de numeros:",
                                 str(CANTIDAD_NUMEROS), 4)

        # 2c) Boton principal.
        f_run = tk.LabelFrame(
            cont, text=" Ejecucion ",
            font=("Segoe UI", 9, "bold"), bg="white", padx=15, pady=10,
        )
        f_run.grid(row=0, column=2, padx=10, sticky="nsew")

        tk.Button(
            f_run, text="CORRER SIMULACION",
            bg="#1b5e20", fg="white", font=("Segoe UI", 11, "bold"),
            command=self.ejecutar, height=3, width=22,
        ).pack(pady=5)

        cont.grid_columnconfigure(0, weight=1)
        cont.grid_columnconfigure(1, weight=1)
        cont.grid_columnconfigure(2, weight=1)

    def _input(self, parent, label, default, row):
        tk.Label(parent, text=label, bg="white",
                 font=("Segoe UI", 9)).grid(row=row, column=0,
                                            sticky="e", pady=2)
        entry = ttk.Entry(parent, width=14, justify="center")
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    # --- 3) Botones secundarios -----------------------------------------
    def _zona_acciones(self):
        barra = tk.Frame(self.root, bg="#eceff1")
        barra.pack(pady=5)

        tk.Button(
            barra, text="Ver pruebas estadisticas",
            bg="#37474f", fg="white", font=("Segoe UI", 9, "bold"),
            command=self.abrir_pruebas, padx=10,
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            barra, text="Exportar todo a Excel (.xlsx)",
            bg="#2e7d32", fg="white", font=("Segoe UI", 9, "bold"),
            command=self.exportar_excel, padx=10,
        ).grid(row=0, column=1, padx=10)

    # --- 4) Indicadores rapidos -----------------------------------------
    def _zona_indicadores(self):
        panel = tk.Frame(self.root, bg="#eceff1")
        panel.pack(fill="x", padx=30, pady=5)

        self.ind_atendidos = self._indicador(panel, "Clientes atendidos", "#2e7d32", 0)
        self.ind_espera = self._indicador(panel, "Espera promedio", "#c62828", 1)
        self.ind_ocio = self._indicador(panel, "Ocio total", "#4527a0", 2)
        self.ind_w = self._indicador(panel, "W (tiempo sistema)", "#0d47a1", 3)
        self.ind_l = self._indicador(panel, "L (clientes sistema)", "#bf360c", 4)

    def _indicador(self, parent, texto, color, col):
        f = tk.Frame(parent, bg="white", relief="solid", bd=1)
        f.grid(row=0, column=col, padx=8, pady=8, sticky="ew")
        parent.columnconfigure(col, weight=1)

        tk.Label(f, text=texto, bg="white",
                 font=("Segoe UI", 9)).pack(pady=(8, 0))
        lbl = tk.Label(f, text="--", bg="white",
                       font=("Segoe UI", 14, "bold"), fg=color)
        lbl.pack(pady=(0, 8))
        return lbl

    # --- 5) Tabla con el paso a paso ------------------------------------
    def _zona_tabla(self):
        marco = tk.LabelFrame(
            self.root, text=" Paso a paso de la simulacion ",
            font=("Segoe UI", 9, "bold"), bg="white", padx=10, pady=5,
        )
        marco.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = (
            "Cliente", "U_lleg", "U_serv", "T_entre", "T_llegada",
            "T_servicio", "Cajero", "T_inicio", "T_fin",
            "T_espera", "T_ocio", "T_sistema",
        )
        self.tree = ttk.Treeview(marco, columns=columnas,
                                 show="headings", height=14)
        for c in columnas:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=85, anchor="center")

        scroll = ttk.Scrollbar(marco, orient="vertical",
                               command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # ==================================================================
    # Acciones de botones
    # ==================================================================
    def ejecutar(self):
        """Genera numeros, valida y corre la simulacion completa."""
        try:
            # 1) Leer parametros del LCG desde la UI.
            x0 = int(self.val_x0.get())
            a = int(self.val_a.get())
            c = int(self.val_c.get())
            m = int(self.val_m.get())
            n = int(self.val_n.get())

            # 2) Generar numeros pseudoaleatorios.
            generador = GeneradorLCG(x0, a, c, m)
            self.numeros = generador.generar(n)

            # 3) Aplicar las 2 pruebas estadisticas.
            self.resultado_medias = st.prueba_medias(self.numeros)
            self.resultado_corridas = st.prueba_corridas(self.numeros)

            # 4) Correr la simulacion del banco.
            sim = SimulacionBanco(self.numeros)
            sim.simular()
            self.registro = sim.registro
            self.resultados = sim.obtener_resultados()

            # 5) Actualizar UI.
            self._actualizar_indicadores()
            self._actualizar_tabla()

            messagebox.showinfo(
                "Exito",
                "Simulacion finalizada.\n"
                f"Clientes atendidos: {self.resultados['atendidos']}",
            )

        except ValueError:
            messagebox.showerror(
                "Error de Parametros",
                "Verifica que los campos del LCG sean numeros enteros validos.",
            )

    def _actualizar_indicadores(self):
        r = self.resultados
        self.ind_atendidos.config(text=f"{r['atendidos']}")
        self.ind_espera.config(text=f"{r['espera_prom']:.3f} min")
        self.ind_ocio.config(text=f"{r['ocio_total']:.2f} min")
        self.ind_w.config(text=f"{r['W']:.3f} min")
        self.ind_l.config(text=f"{r['L']:.3f}")

    def _actualizar_tabla(self):
        # Limpiar tabla anterior.
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insertar registros nuevos.
        for fila in self.registro:
            self.tree.insert("", "end", values=list(fila.values()))

    # ------------------------------------------------------------------
    # Ventana de pruebas estadisticas (Notebook)
    # ------------------------------------------------------------------
    def abrir_pruebas(self):
        if not self.numeros:
            messagebox.showwarning(
                "Atencion",
                "Primero ejecuta la simulacion para tener numeros que evaluar.",
            )
            return

        vent = tk.Toplevel(self.root)
        vent.title("Reporte de validacion estadistica")
        vent.geometry("680x400")
        vent.configure(bg="#f5f5f5")

        nb = ttk.Notebook(vent)
        nb.pack(pady=10, padx=20, expand=True, fill="both")

        # Pestaña 1: Prueba de Medias.
        m = self.resultado_medias
        tab1 = tk.Frame(nb, bg="white", padx=20, pady=20)
        nb.add(tab1, text="Prueba de Medias")
        info_medias = (
            "Hipotesis: la media de los U_i tiende a 0.5 (uniformidad).\n\n"
            f"Cantidad de numeros (n)    : {len(self.numeros)}\n"
            f"Media calculada            : {m['media']:.6f}\n"
            f"Limite inferior aceptacion : {m['limite_inferior']:.6f}\n"
            f"Limite superior aceptacion : {m['limite_superior']:.6f}\n"
            f"Z critico (alpha=0.05)     : {st.Z_CRITICO}\n"
        )
        tk.Label(tab1, text=info_medias, justify="left",
                 font=("Consolas", 11), bg="white").pack(anchor="w")
        self._etiqueta_veredicto(tab1, m["aprobada"])

        # Pestaña 2: Prueba de Corridas.
        c = self.resultado_corridas
        tab2 = tk.Frame(nb, bg="white", padx=20, pady=20)
        nb.add(tab2, text="Prueba de Corridas")
        info_cor = (
            "Hipotesis: los U_i son independientes entre si.\n\n"
            f"Corridas observadas (c0) : {c['corridas']}\n"
            f"Media esperada (mu)      : {c['media_esperada']:.4f}\n"
            f"Varianza                 : {c['varianza']:.4f}\n"
            f"Z0 calculado             : {c['z0']:.4f}\n"
            f"Z critico (alpha=0.05)   : {c['z_critico']}\n"
        )
        tk.Label(tab2, text=info_cor, justify="left",
                 font=("Consolas", 11), bg="white").pack(anchor="w")
        self._etiqueta_veredicto(tab2, c["aprobada"])

    def _etiqueta_veredicto(self, parent, aprobada):
        texto = "APROBADA" if aprobada else "RECHAZADA"
        color = "#2e7d32" if aprobada else "#c62828"
        tk.Label(parent, text=texto, font=("Segoe UI", 16, "bold"),
                 bg="white", fg=color).pack(pady=15)

    # ------------------------------------------------------------------
    # Exportacion a Excel (varias hojas)
    # ------------------------------------------------------------------
    def exportar_excel(self):
        if not self.registro:
            messagebox.showwarning(
                "Error", "No hay datos para exportar. Ejecuta la simulacion.",
            )
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile="simulacion_banco_5_13.xlsx",
        )
        if not ruta:
            return

        # Hoja "Configuracion": parametros del LCG y del problema.
        config = pd.DataFrame({
            "Parametro": [
                "Semilla X0", "Multiplicador a", "Incremento c", "Modulo m",
                "Cantidad de numeros",
                "Cajeros", "Tasa llegada (clientes/h)",
                "Media interarribo (min)",
                "Servicio min (min)", "Servicio max (min)",
            ],
            "Valor": [
                int(self.val_x0.get()), int(self.val_a.get()),
                int(self.val_c.get()), int(self.val_m.get()),
                int(self.val_n.get()),
                NUM_CAJEROS, TASA_LLEGADA_HORA, MEDIA_INTERARRIBO,
                SERV_MIN, SERV_MAX,
            ],
        })

        # Hoja "Numeros LCG": los U_i generados.
        numeros = pd.DataFrame({
            "i": list(range(1, len(self.numeros) + 1)),
            "U_i": self.numeros,
        })

        # Hoja "Simulacion": paso a paso por cliente.
        sim = pd.DataFrame(self.registro)

        # Hoja "Pruebas": veredictos de medias y corridas.
        m = self.resultado_medias
        c = self.resultado_corridas
        pruebas = pd.DataFrame({
            "Prueba": ["Medias", "Corridas"],
            "Estadistico": [m["media"], c["z0"]],
            "Limite/Critico": [
                f"[{m['limite_inferior']:.4f}, {m['limite_superior']:.4f}]",
                f"+/- {c['z_critico']}",
            ],
            "Resultado": [
                "APROBADA" if m["aprobada"] else "RECHAZADA",
                "APROBADA" if c["aprobada"] else "RECHAZADA",
            ],
        })

        # Hoja "Resultados": W, L y demas indicadores finales.
        r = self.resultados
        resultados = pd.DataFrame({
            "Indicador": [
                "Clientes atendidos", "Espera promedio (min)",
                "Ocio total (min)", "W (tiempo en sistema, min)",
                "L (clientes en sistema)",
            ],
            "Valor": [
                r["atendidos"], r["espera_prom"],
                r["ocio_total"], r["W"], r["L"],
            ],
        })

        with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
            config.to_excel(writer, sheet_name="Configuracion", index=False)
            numeros.to_excel(writer, sheet_name="Numeros LCG", index=False)
            sim.to_excel(writer, sheet_name="Simulacion", index=False)
            pruebas.to_excel(writer, sheet_name="Pruebas", index=False)
            resultados.to_excel(writer, sheet_name="Resultados", index=False)

        messagebox.showinfo("Guardado", f"Archivo exportado:\n{ruta}")


# ----- Punto de entrada -----
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    InterfazSimulador(root)
    root.mainloop()
