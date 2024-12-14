import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_polynomial():
    """Obtiene el polinomio del usuario y lo evalúa."""
    try:
        polynomial_str = polynomial_entry.get()
        f = eval("lambda x1, x2: " + polynomial_str)
        return f
    except Exception as e:
        messagebox.showerror("Error", f"Error en el polinomio: {e}")
        return None


def get_ranges():
    """Obtiene los rangos ingresados por el usuario."""
    try:
        x1_min, x1_max, x1_step = map(float, x1_range_entry.get().split(","))
        x2_min, x2_max, x2_step = map(float, x2_range_entry.get().split(","))
        x1 = np.arange(x1_min, x1_max, x1_step)
        x2 = np.arange(x2_min, x2_max, x2_step)
        return x1, x2
    except Exception as e:
        messagebox.showerror("Error", f"Error en los rangos: {e}")
        return None, None


def generate_graphs():
    """Genera los dos gráficos al iniciar la aplicación."""
    global fig_3d, fig_contour

    polynomial = get_polynomial()
    x1, x2 = get_ranges()

    if polynomial and x1 is not None and x2 is not None:
        X1, X2 = np.meshgrid(x1, x2)
        Z = polynomial(X1, X2)

        # Gráfico 3D
        fig_3d = plt.Figure(figsize=(5, 5), dpi=100)
        ax_3d = fig_3d.add_subplot(111, projection="3d")
        ax_3d.plot_surface(X1, X2, Z, cmap=cm.cividis)
        ax_3d.set_xlabel("x1")
        ax_3d.set_ylabel("x2")
        ax_3d.set_zlabel("Z")

        # Gráfico de Contorno
        fig_contour = plt.Figure(figsize=(5, 5), dpi=100)
        ax_contour = fig_contour.add_subplot(111)
        contour = ax_contour.contourf(X1, X2, Z, cmap=cm.rainbow)
        fig_contour.colorbar(contour)

    else:
        messagebox.showerror("Error", "Ingrese un polinomio y rangos válidos.")


def show_3d_graph():
    """Muestra el gráfico 3D."""
    global canvas_3d, canvas_contour

    # Ocultar gráfico de contorno si existe
    if canvas_contour:
        canvas_contour.get_tk_widget().pack_forget()

    # Crear o mostrar gráfico 3D
    canvas_3d = FigureCanvasTkAgg(fig_3d, master=canvas_frame)
    canvas_3d.draw()
    canvas_3d.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def show_contour_graph():
    """Muestra el gráfico de contorno."""
    global canvas_3d, canvas_contour

    # Ocultar gráfico 3D si existe
    if canvas_3d:
        canvas_3d.get_tk_widget().pack_forget()

    # Crear o mostrar gráfico de contorno
    canvas_contour = FigureCanvasTkAgg(fig_contour, master=canvas_frame)
    canvas_contour.draw()
    canvas_contour.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def reset_inputs():
    """Borra los gráficos y restablece los datos de entrada a los valores predeterminados."""
    global canvas_3d, canvas_contour

    # Eliminar gráficos si existen
    if canvas_3d:
        canvas_3d.get_tk_widget().pack_forget()
        canvas_3d = None
    if canvas_contour:
        canvas_contour.get_tk_widget().pack_forget()
        canvas_contour = None

    # Restablecer los datos de entrada a sus valores predeterminados
    polynomial_entry.delete(0, tk.END)
    polynomial_entry.insert(0, "17.73 + 0.025*x1 + 0.400*x2 - 1.84*x1**2 - 1.89*x2**2 + 0.25*x1*x2")

    x1_range_entry.delete(0, tk.END)
    x1_range_entry.insert(0, "-1,1,0.01")

    x2_range_entry.delete(0, tk.END)
    x2_range_entry.insert(0, "-1,1,0.01")


# Crear ventana principal
window = tk.Tk()
window.title("Generador de Gráficos")

# Instrucciones
instructions_label = tk.Label(window, text="Introduce el polinomio y los rangos:", font=("Arial", 12))
instructions_label.pack()

# Entrada para el polinomio
polynomial_label = tk.Label(window, text="Polinomio:")
polynomial_label.pack()
polynomial_entry = tk.Entry(window, width=50)
polynomial_entry.insert(0, "17.73 + 0.025*x1 + 0.400*x2 - 1.84*x1**2 - 1.89*x2**2 + 0.25*x1*x2")
polynomial_entry.pack()

# Entrada para los rangos de x1
x1_range_label = tk.Label(window, text="Rango para x1 (min,max,paso):")
x1_range_label.pack()
x1_range_entry = tk.Entry(window, width=50)
x1_range_entry.insert(0, "-1,1,0.01")
x1_range_entry.pack()

# Entrada para los rangos de x2
x2_range_label = tk.Label(window, text="Rango para x2 (min,max,paso):")
x2_range_label.pack()
x2_range_entry = tk.Entry(window, width=50)
x2_range_entry.insert(0, "-1,1,0.01")
x2_range_entry.pack()

# Botones para alternar entre gráficos
button_frame = tk.Frame(window)
button_frame.pack(side=tk.TOP, fill=tk.X)

button_3d = tk.Button(button_frame, text="Mostrar Gráfico 3D", command=show_3d_graph)
button_3d.pack(side=tk.LEFT, padx=10)

button_contour = tk.Button(button_frame, text="Mostrar Gráfico de Contorno", command=show_contour_graph)
button_contour.pack(side=tk.LEFT, padx=10)

button_reset = tk.Button(button_frame, text="Borrar", command=reset_inputs, bg="red", fg="white")
button_reset.pack(side=tk.LEFT, padx=10)

# Frame para los gráficos
canvas_frame = tk.Frame(window)
canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Variables globales para los gráficos
fig_3d = None
fig_contour = None
canvas_3d = None
canvas_contour = None

# Generar gráficos al iniciar
generate_graphs()

# Iniciar la aplicación
window.mainloop()
