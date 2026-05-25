import pandas as pd
import matplotlib.pyplot as plt
# Leer archivo Excel
df = pd.read_excel("inventario_ml JMS.xlsx")
# Convertir columnas a número
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
# Converitr FECHA a formato fecha
df["FECHA"] = pd.to_datetime(df["FECHA"])
# Agrupar ventas por fecha
ventas_por_fecha = df.groupby("FECHA")["SALIDA"].sum()
# Mostrar datos
print("\n=== VENTAS POR FECHA ===\n")
print(ventas_por_fecha)
# Crear gráfica 
plt.figure(figsize=(10,5))
plt.plot(ventas_por_fecha.index, ventas_por_fecha.values, marker='o')
plt.title("Tendencia de Ventas")
plt.xlabel("Fecha")
plt.ylabel("Cantidad Vendida")
plt.grid(True)
plt.tight_layout()
plt.show()