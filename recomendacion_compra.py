import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
# Leer Excel
df = pd.read_excel("inventario_ml JMS.xlsx")
# Convertir columnas
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
df["ENTRADA"] = pd.to_numeric(df["ENTRADA"], errors="coerce")
df["FECHA"] = pd.to_datetime(df["FECHA"])
# Calcular stock actual
df["STOCK"] = df["ENTRADA"] - df["SALIDA"]
# Lista de productos
productos = df["PRODUCTO"].unique()
print("\n=== RECOMENDACION INTELIGENTE DE COMPRA ===\n")
# Analizar cada producto
for producto in productos:
    datos_producto = df[df["PRODUCTO"] == producto]
    # Ventas por fecha
    ventas = datos_producto.groupby("FECHA")["SALIDA"].sum().reset_index()
    # Crear días
    ventas["DIAS"] = np.arange(len(ventas))
    X = ventas[["DIAS"]]
    y = ventas["SALIDA"]
    # Stock actual
    stock_actual = datos_producto["STOCK"].sum()
    if len(ventas) > 1:
        # Modelo ML
        modelo = LinearRegression()
        modelo.fit(X, y)
        # Predecir siguiente día
        siguiente_dia = pd.DataFrame({"DIAS": [len(ventas)]})
        prediccion = modelo.predict(siguiente_dia)[0]
        # Recomendación
        diferencia = prediccion - stock_actual
        print(f"\n📦 {producto}")
        print(f"Stock actual: {stock_actual:.0f}")
        print(f"Ventas estimadas: {prediccion:.0f}")
        if diferencia > 0:
            print(f"🚨 Recomendación: comprar {abs(diferencia):.0f} unidades")
        else:
            print("✅ Stock suficiente")