import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Configuración página
st.set_page_config(page_title="Dashboard Inteligente", layout="wide")
# Título
st.title("📦 Dashboard Inteligente de Inventario")
# Leer Excel
df = pd.read_excel("inventario_ml JMS.xlsx")
# Convertir columnas
df["SALIDA"] = pd.to_numeric(df["SALIDA"], errors="coerce")
df["ENTRADA"] = pd.to_numeric(df["ENTRADA"], errors="coerce")
df["PRECIO"] = pd.to_numeric(df["PRECIO"], errors="coerce")
# Calcular ingresos
df["INGRESOS"] = df["SALIDA"] * df["PRECIO"]
# Calcular stock
df["STOCK"] = df["ENTRADA"] - df["SALIDA"]
# =========================
# FILTRO PRODUCTOS
# =========================
productos = st.sidebar.multiselect("Selecciona productos", df["PRODUCTO"].unique(), default=df["PRODUCTO"].unique())
df_filtrado = df[df["PRODUCTO"].isin(productos)]
# =========================
# KPIs
# =========================
ventas_totales = df_filtrado["SALIDA"].sum()
ingresos_totales = df_filtrado["INGRESOS"].sum()
stock_total = df_filtrado["STOCK"].sum()
col1, col2, col3 = st.columns(3)
col1.metric("📈 Ventas Totales", f"{ventas_totales:.0f}")
col2.metric("💰 Ingresos Totales", f"${ingresos_totales:,.0f}")
col3.metric("📦 Stock Total", f"{stock_total:.0f}")
# =========================
# TABLA
# =========================
st.subheader("📋 Inventario")
st.dataframe(df_filtrado)
# =========================
# PRODUCTOS MÁS VENDIDOS
# =========================
ventas_producto = df_filtrado.groupby("PRODUCTO")["SALIDA"].sum()
st.subheader("📈 Productos Más Vendidos")
fig1, ax1 = plt.subplots(figsize=(10,5))
ax1.bar(ventas_producto.index, ventas_producto.values)
plt.xticks(rotation=90)
st.pyplot(fig1)
# =========================
# RENTABILIDAD
# =========================
rentabilidad = df_filtrado.groupby("PRODUCTO")["INGRESOS"].sum()
st.subheader("💰 Productos Más Rentables")
fig2, ax2 = plt.subplots(figsize=(10,5))
ax2.bar(rentabilidad.index, rentabilidad.values)
plt.xticks(rotation=90)
st.pyplot(fig2)
# =========================
# CLASIFICACION ABC
# =========================
st.subheader("🧠 Clasificación ABC")
clasificacion = rentabilidad.sort_values(ascending=False)
for producto, ingreso in clasificacion.items():
    if ingreso >= 3000000:
        st.success(f"{producto} → Clase A")
    elif ingreso >= 1000000:
        st.warning(f"{producto} → Clase B")
    else:
        st.error(f"{producto} → Clase C")
# =========================
# ALERTAS DE STOCK
# =========================
st.subheader("🚨 Alertas de Stock")
stock_producto = df_filtrado.groupby("PRODUCTO")["STOCK"].sum()
for producto, stock in stock_producto.items():
    if stock <= 20:
        st.error(f"{producto}: STOCK CRÍTICO ({stock} unidades)")
    elif stock <= 50:
        st.warning(f"{producto}: STOCK BAJO ({stock} unidades)")
    else:
        st.success(f"{producto}: Stock suficiente ({stock} unidades)")