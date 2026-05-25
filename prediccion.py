import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
# Leer Excel
df = pd.read_excel("inventario_ml JMS.xlsx")
# Convertir columnas
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
df["FECHA"] = pd.to_datetime(df["FECHA"])
# Agrupar ventas por fecha
ventas_por_fecha = df.groupby("FECHA")["SALIDA"].sum().reset_index()
# Convertir fechas a números
ventas_por_fecha["DIAS"] = np.arange(len(ventas_por_fecha))
# Variables para ML
X = ventas_por_fecha[["DIAS"]]
y = ventas_por_fecha["SALIDA"]
# Crear modelo
modelo = LinearRegression()
# Entrenar modelo
modelo.fit(X, y)
# Predecir siguiente día
siguiente_dia = np.array([[len(ventas_por_fecha)]])
prediccion = modelo.predict(siguiente_dia)
# Mostrar predicción
print("\n=== PREDICCION DE VENTAS ===\n")
print(f"Ventas estimadas para el siguiente día: {prediccion[0]:.2f}")
# Graficar datos reales
plt.figure(figsize=(10,5))
plt.plot(ventas_por_fecha["DIAS"], ventas_por_fecha["SALIDA"], marker='o', label="Ventas Reales")
# Graficar predicción
plt.scatter(siguiente_dia, prediccion, label="Prediccion")
plt.title("Prediccion de Ventas")
plt.xlabel("Dias")
plt.ylabel("Ventas")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()