import pandas as pd
import matplotlib.pyplot as plt
# Leer archivo Excel
df = pd.read_excel("inventario accesorios JMS.xlsx")
# Convertir SALIDA a número
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
# Ordenar productos por salida
top_productos = df.sort_values(by="SALIDA", ascending=False)
# Mostrar inventario
print("\n=== INVENTARIO COMPLETO ===\n")
print(df)
# Productos con stock bajo
stock_bajo = df[df["Unidades"] < 5]
print("\n=== PRODUCTOS CON STOCK BAJO ===\n")
print(stock_bajo)
# Mostrar productos con alta rotación
alta_rotacion = df[df["SALIDA"] > 50]
print("\n=== PRODUCTOS DE ALTA ROTACION ===\n")
print(alta_rotacion)
# Crear gráfica
plt.figure(figsize=(12,6))
plt.bar(top_productos["Producto"], top_productos["SALIDA"])
plt.xticks(rotation=90)
plt.title("Productos con Mayor Rotacion")
plt.xlabel("Productos")
plt.ylabel("Cantidad Vendida")
plt.tight_layout()
plt.show()