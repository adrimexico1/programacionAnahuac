import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import tkinter as tk
from tkinter import messagebox

# Leer el archivo XLSX
file_path = 'Evolucion_IPC_esp.xlsx'
df = pd.read_excel(file_path)

# Limpiar los nombres de las columnas eliminando espacios extra
df.columns = df.columns.str.strip()

# Convertir la columna 'Periodo' a tipo datetime
df['Periodo'] = pd.to_datetime(df['Periodo'], format='%d/%m/%y', errors='coerce')

# Comprobar si la conversión fue exitosa
if df['Periodo'].isnull().any():
    print("Algunos valores en la columna 'Periodo' no pudieron convertirse a datetime.")
    print(df[df['Periodo'].isnull()])
else:
    print("Conversión de 'Periodo' a datetime exitosa.")

# Establecer 'Periodo' como índice de fechas
df.set_index('Periodo', inplace=True)

# Asegurarnos de que el índice sea un DatetimeIndex y establecer la frecuencia mensual (MS)
df.index = pd.to_datetime(df.index)
df.index.freq = 'MS'  # Establecer la frecuencia mensual (inicio de mes)

# Lista de las columnas a mostrar en los botones
columnas = [
    'Bebidas alcohólicas y tabaco',
    'Vestido y calzado',
    'Vivienda',
    'Menaje del hogar',
    'Medicina',
    'Transportes',
    'Comunicaciones',
    'Ocio y cultura',
    'Hoteles, cafés y restaurantes',
    'Otros bienes y servicios'
]

# Función para generar la gráfica de SARIMA
def generar_grafica(columna):
    try:
        serie_temporal = df[columna].dropna()  # Eliminar valores nulos

        # Verificar si el índice es datetime
        if not isinstance(serie_temporal.index, pd.DatetimeIndex):
            raise ValueError("El índice de fechas no es del tipo DatetimeIndex.")

        # Ajustar el modelo SARIMA
        sarima_model = SARIMAX(serie_temporal, 
                               order=(1, 1, 1),  # Orden del modelo ARIMA
                               seasonal_order=(1, 1, 1, 12),  # Estacionalidad con período 12 (mensual)
                               enforce_stationarity=False, 
                               enforce_invertibility=False)

        # Ajustar el modelo
        sarima_fit = sarima_model.fit(disp=False, maxiter=1000)

        # Predicción futura (10 años)
        pred = sarima_fit.get_forecast(steps=120)  # 120 meses = 10 años
        pred_mean = pred.predicted_mean
        pred_conf_int = pred.conf_int()

        # Graficar los resultados
        plt.figure(figsize=(10, 6))
        plt.plot(serie_temporal, label='Datos Históricos', color='blue')
        plt.plot(pred_mean.index, pred_mean, label='Predicción a Futuro (10 años)', color='red')
        plt.fill_between(pred_conf_int.index, pred_conf_int.iloc[:, 0], pred_conf_int.iloc[:, 1], color='red', alpha=0.3)
        plt.title(f'Predicción SARIMA para: {columna}')
        plt.xlabel('Fecha')
        plt.ylabel('Valor')
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al generar la gráfica: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gráficas de Predicción SARIMA")

# Crear botones en una cuadrícula
frame = tk.Frame(ventana)
frame.pack(pady=10)

for i, columna in enumerate(columnas):
    boton = tk.Button(frame, text=columna, command=lambda c=columna: generar_grafica(c))
    boton.grid(row=i // 2, column=i % 2, padx=10, pady=5)  # Organizar en 2 columnas

# Ejecutar la interfaz gráfica
ventana.mainloop()

