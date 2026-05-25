import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
# Leer Excel
df = pd.read_excel("inventario_ml JMS.xlsx")
# Convertir columnas
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
df["FECHA"] = pd.to_datetime(df["FECHA"])
# Lista de productos únicos
productos = df["PRODUCTO"].unique()
print("\n=== PREDICCION POR PRODUCTO ===\n")
# Hacer predicción para cada producto
for producto in productos:
    # Filtrar producto
    datos_producto = df[df["PRODUCTO"] == producto]
    # Agrupar ventas por fecha
    ventas = datos_producto.groupby("FECHA")["SALIDA"].sum().reset_index()
    # Crear columna de días
    ventas["DIAS"] = np.arange(len(ventas))
    # Variables ML
    X = ventas[["DIAS"]]
    y = ventas["SALIDA"]
    # Verificar suficientes datos
    if len(ventas) > 1:
        # Crear modelo
        modelo = LinearRegression()
        # Entrenar
        modelo.fit(X, y)
        # Predecir siguiente día
        siguiente_dia = pd.DataFrame({"DIAS": [len(ventas)]})
        prediccion = modelo.predict(siguiente_dia)
        # Mostrar resultado
        print(f"{producto}: {prediccion[0]:.2f} ventas estimadas")