import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# Función para ejecutar la simulación
def run_simulation():
    try:
        # Obtener los valores de entrada
        lsr = float(entry_lsr.get())
        rs = float(entry_rs.get())
        acid_concentration = float(entry_acid.get())
        residence_time = float(entry_residence.get())

        # Parámetros cinéticos y constantes
        kH0 = 7.709e8
        EH = 20301.9
        βH = 1
        R = 1.98
        kX0 = 2.6e8
        EX = 20312
        βX = 0.15
        T = 121.1 + 273.15
        ρa = 1.84

        # Cálculo del factor Φ
        RL = lsr * ρa
        Φ = RL / rs

        # Definir las ecuaciones diferenciales
        def acidH(t, u):
            du1 = -kH0 * acid_concentration**βH * np.exp(-(EH / (R * T))) * u[0] * Φ
            du2 = (
                kH0 * acid_concentration**βH * np.exp(-(EH / (R * T))) * u[0] * Φ
                - kX0 * acid_concentration**βX * np.exp(-(EX / (R * T))) * u[1] * Φ
            )
            du3 = (
                kH0 * acid_concentration**βH * np.exp(-(EH / (R * T))) * u[0]
                - kX0
                * acid_concentration**βX
                * np.exp(-(EX / (R * T)))
                * u[1]
                * 0.7
                * Φ
            )
            return [du1, du2, du3]

        # Condiciones iniciales
        u0 = [70, 0, 0]
        t_span = (0, residence_time)
        t_eval = np.linspace(0, residence_time, 100)

        # Resolver las ecuaciones diferenciales
        solution = solve_ivp(acidH, t_span, u0, method="RK45", t_eval=t_eval)

        # Graficar los resultados
        ax.clear()
        ax.plot(solution.t, solution.y[0], label="Hemicelulosa", color="blue")
        ax.plot(solution.t, solution.y[1], label="Xilosa", color="green")
        ax.plot(solution.t, solution.y[2], label="Furfural", color="red")
        ax.set_title("Resultados de la Simulación")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Concentraciones")
        ax.legend()
        canvas.draw()

        # Guardar los datos en variables globales
        global simulation_data
        simulation_data = pd.DataFrame(
            {
                "Tiempo": solution.t,
                "Hemicelulosa": solution.y[0],
                "Xilosa": solution.y[1],
                "Furfural": solution.y[2],
            }
        )

        # Mostrar mensaje de éxito
        messagebox.showinfo("Simulación", "Simulación completada exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")


# Función para exportar datos a CSV
def export_to_csv():
    if simulation_data is not None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if file_path:
            simulation_data.to_csv(file_path, index=False)
            messagebox.showinfo("Exportación", "Datos exportados exitosamente.")
    else:
        messagebox.showwarning("Exportación", "No hay datos para exportar.")


# Función para reiniciar los valores de entrada
def reset_inputs():
    entry_lsr.delete(0, tk.END)
    entry_rs.delete(0, tk.END)
    entry_acid.delete(0, tk.END)
    entry_residence.delete(0, tk.END)
    entry_lsr.insert(0, "10")
    entry_rs.insert(0, "5")
    entry_acid.insert(0, "0.5")
    entry_residence.insert(0, "10")
    ax.clear()
    canvas.draw()


# Configuración de la ventana principal
root = tk.Tk()
root.title("ACIDHYDROCHEM Simulator V0.1")
root.geometry("800x600")

# Marco para los controles
frame_controls = ttk.Frame(root)
frame_controls.pack(side=tk.LEFT, padx=10, pady=10)

# Controles de entrada
ttk.Label(frame_controls, text="Razón Líquido/Sólido (kg):").pack(pady=5)
entry_lsr = ttk.Entry(frame_controls)
entry_lsr.pack()
entry_lsr.insert(0, "10")

ttk.Label(frame_controls, text="Razón Sólido:").pack(pady=5)
entry_rs = ttk.Entry(frame_controls)
entry_rs.pack()
entry_rs.insert(0, "5")

ttk.Label(frame_controls, text="Concentración Ácida:").pack(pady=5)
entry_acid = ttk.Entry(frame_controls)
entry_acid.pack()
entry_acid.insert(0, "0.5")

ttk.Label(frame_controls, text="Tiempo de Residencia:").pack(pady=5)
entry_residence = ttk.Entry(frame_controls)
entry_residence.pack()
entry_residence.insert(0, "10")

# Botones
ttk.Button(frame_controls, text="Simular", command=run_simulation).pack(pady=10)
ttk.Button(frame_controls, text="Exportar CSV", command=export_to_csv).pack(pady=10)
ttk.Button(frame_controls, text="Reiniciar", command=reset_inputs).pack(pady=10)
# Botón para cerrar el programa
ttk.Button(frame_controls, text="Cerrar", command=root.destroy).pack(pady=10)


# Espacio para el gráfico
frame_graph = ttk.Frame(root)
frame_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Variable global para almacenar los datos de simulación
simulation_data = None

# Iniciar el bucle principal de Tkinter
root.mainloop()
