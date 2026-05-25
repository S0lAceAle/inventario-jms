import pandas as pd
import matplotlib.pyplot as plt
# Leer archivo Excel
df = pd.read_excel("inventario_ml JMS.xlsx")
# Convertir columnas a número
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
df["PRECIO"] = pd.to_numeric(df["PRECIO"], errors="coerce")
# Calcular ingresos
df["INGRESOS"] = df["SALIDA"] * df["PRECIO"]
# Agrupar ingresos por producto
ingresos_producto = df.groupby("PRODUCTO")["INGRESOS"].sum()
# Ordenar de mayor a menor
ingresos_producto = ingresos_producto.sort_values(ascending=False)
# Mostrar resultados
print("\n=== PRODUCTOS MAS RENTABLES ===\n")
print(ingresos_producto)
# Crear gráfica
plt.figure(figsize=(12,6))
plt.bar(ingresos_producto.index, ingresos_producto.values)
plt.xticks(rotation=90)
plt.title("Productos Mas Rentables")
plt.xlabel("Producto")
plt.ylabel("Ingresos")
plt.tight_layout()
plt.show()