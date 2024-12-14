import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta

# Cargar el archivo CSV
df = pd.read_csv("[Registro TA]20231224-20241206.csv")

# Limpiar los nombres de las columnas (eliminar espacios extra)
df.columns = df.columns.str.strip()

# Convertir la columna 'Fecha de medición' a tipo datetime
df['Fecha de medición'] = pd.to_datetime(df['Fecha de medición'])

# Establecer la columna 'Fecha de medición' como índice
df.set_index('Fecha de medición', inplace=True)

# Definir las series temporales para SYS, DIA y Pulso
sys = df['SYS']
dia = df['DIA']
pulso = df['Pulso']

# Función para ajustar y predecir con SARIMA
def sarima_predict(series, steps=365):
    # Ajustar el modelo SARIMA
    model = SARIMAX(series, 
                    order=(1, 1, 1),  # (p, d, q)
                    seasonal_order=(1, 1, 1, 12),  # (P, D, Q, S) con S=12 para estacionalidad anual
                    enforce_stationarity=False, 
                    enforce_invertibility=False)
    
    # Entrenar el modelo
    model_fit = model.fit(disp=False)
    
    # Realizar la predicción
    forecast = model_fit.get_forecast(steps=steps)
    
    # Obtener los intervalos de confianza de la predicción
    pred_conf = forecast.conf_int()
    
    return forecast.predicted_mean, pred_conf

# Función para agregar ruido
def add_noise_to_predictions(predictions, std_dev=5):
    """ Agrega ruido aleatorio a las predicciones para hacerlas más realistas """
    noise = np.random.normal(loc=0, scale=std_dev, size=len(predictions))
    return predictions + noise

# Realizar la predicción para SYS, DIA y Pulso a 1 año (365 días)
sys_pred, sys_conf = sarima_predict(sys)
dia_pred, dia_conf = sarima_predict(dia)
pulso_pred, pulso_conf = sarima_predict(pulso)

# Agregar ruido para hacer las predicciones más realistas
sys_pred_noisy = add_noise_to_predictions(sys_pred)
dia_pred_noisy = add_noise_to_predictions(dia_pred)
pulso_pred_noisy = add_noise_to_predictions(pulso_pred)

# Crear un índice para los días futuros
future_dates = pd.date_range(df.index[-1] + timedelta(days=1), periods=365, freq='D')

# Graficar las predicciones en una sola gráfica
plt.figure(figsize=(10, 6))

# Graficar SYS, DIA y Pulso con ruido agregado
plt.plot(df.index, sys, label='SYS', color='blue', linestyle='-', linewidth=2)
plt.plot(future_dates, sys_pred_noisy, label='Predicción SYS con Ruido', color='cyan', linestyle='--', linewidth=2)
plt.fill_between(future_dates, sys_conf.iloc[:, 0], sys_conf.iloc[:, 1], color='cyan', alpha=0.3)

plt.plot(df.index, dia, label='DIA', color='red', linestyle='-', linewidth=2)
plt.plot(future_dates, dia_pred_noisy, label='Predicción DIA con Ruido', color='pink', linestyle='--', linewidth=2)
plt.fill_between(future_dates, dia_conf.iloc[:, 0], dia_conf.iloc[:, 1], color='pink', alpha=0.3)

plt.plot(df.index, pulso, label='Pulso', color='green', linestyle='-', linewidth=2)
plt.plot(future_dates, pulso_pred_noisy, label='Predicción Pulso con Ruido', color='lightgreen', linestyle='--', linewidth=2)
plt.fill_between(future_dates, pulso_conf.iloc[:, 0], pulso_conf.iloc[:, 1], color='lightgreen', alpha=0.3)

# Limitar el rango del eje y (valores)
plt.ylim(0, 200)  # Mostrar valores entre 0 y 200

# Añadir título y etiquetas
plt.title('Predicción de SYS, DIA y Pulso para 1 año (Con Ruido)')
plt.xlabel('Fecha')
plt.ylabel('Valores')
plt.legend()

# Mostrar la gráfica
plt.tight_layout()
plt.show()
