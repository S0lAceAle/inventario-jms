import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Dashboard Operativo", layout="wide")
# =========================
# TÍTULO
# =========================
st.title("📦 Dashboard Operativo de Inventario")
# =========================
# LEER EXCEL
# =========================
df = pd.read_excel("inventario accesorios JMS.xlsx")
# =========================
# CONVERTIR COLUMNAS
# =========================
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
df["ENTRADA"] = pd.to_numeric(df["ENTRADA"], errors="coerce")
df["Unidades"] = pd.to_numeric(df["Unidades"], errors="coerce")
# =========================
# KPIs
# =========================
total_productos = len(df)
stock_total = df["Unidades"].sum()
ventas_totales = df["SALIDA"].sum()
col1, col2, col3 = st.columns(3)
col1.metric("📦 Productos", total_productos)
col2.metric("📈 Ventas Totales", f"{ventas_totales:.0f}")
col3.metric("🏪 Stock Total", f"{stock_total:.0f}")
# =========================
# INVENTARIO COMPLETO
# =========================
st.subheader("📋 Inventario Completo")
st.dataframe(df)
# =========================
# STOCK BAJO
# =========================
st.subheader("🚨 Productos con Stock Bajo")
stock_bajo = df[df["Unidades"] <= 5]
if len(stock_bajo) > 0:
    st.dataframe(stock_bajo)
else:
    st.success("✅ No hay productos con stock bajo")
# =========================
# ALTA ROTACIÓN
# =========================
st.subheader("🔥 Productos con Alta Rotación")
alta_rotacion = df[df["SALIDA"] >= 50]
if len(alta_rotacion) > 0:
    st.dataframe(alta_rotacion)
else:
    st.warning("No hay productos con alta rotación")
# =========================
# GRÁFICA
# =========================
st.subheader("📊 Ventas por Producto")
ventas_producto = df.groupby("Producto")["SALIDA"].sum()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(ventas_producto.index, ventas_producto.values)
plt.xticks(rotation=90)
st.pyplot(fig)