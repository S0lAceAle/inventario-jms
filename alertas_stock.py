import pandas as pd
# Leer Excel
df = pd.read_excel("inventario_ml JMS.xlsx")
# Convertir columnas
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
df["ENTRADA"] = pd.to_numeric(df["ENTRADA"], errors="coerce")
# Calcular stock estimado
df["STOCK_ESTIMADO"] = df["ENTRADA"] - df["SALIDA"]
# Agrupar stock por producto
stock_producto = df.groupby("PRODUCTO")["STOCK_ESTIMADO"].sum()
print("\n=== ALERTAS DE STOCK ===\n")
# Revisar productos
for producto, stock in stock_producto.items():
    if stock <= 20:
        print(f"🚨 {producto}: STOCK CRITICO ({stock} unidades)")
    elif stock <= 50:
        print(f"⚠️ {producto}: STOCK BAJO ({stock} unidades)")
    else:
        print(f"✅ {producto}: Stock suficiente ({stock} unidades)")