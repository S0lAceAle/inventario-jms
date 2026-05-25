import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# --- Configuración de Firebase ---
# Asegúrate de que tu archivo serviceAccountKey.json esté en el mismo directorio
# o proporciona la ruta completa a tu archivo JSON de credenciales.
# Si estás implementando esto en un entorno como Streamlit Cloud,
# deberías usar st.secrets para almacenar de forma segura tus credenciales.

# Comprueba si Firebase ya ha sido inicializado para evitar errores en re-runs
if not firebase_admin._apps:
    try:
        # Intenta cargar las credenciales desde un archivo local
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    except FileNotFoundError:
        st.error("Error: serviceAccountKey.json no encontrado. "
                 "Asegúrate de que el archivo JSON de tus credenciales de Firebase "
                 "esté en el mismo directorio que este script o proporciona la ruta correcta.")
        st.stop()
    except Exception as e:
        st.error(f"Error al inicializar Firebase: {e}")
        st.stop()

db = firestore.client()

# --- Funciones de Firestore ---

def get_products():
    """Recupera todos los productos de la colección 'products' en Firestore."""
    products_ref = db.collection('inventario')
    docs = products_ref.stream()
    products_list = []
    for doc in docs:
        product_data = doc.to_dict()
        product_data['id'] = doc.id # Añadir el ID del documento
        products_list.append(product_data)
    return products_list

def add_product(name, stock, price):
    """Agrega un nuevo producto a la colección 'products' en Firestore."""
    try:
        doc_ref = db.collection('inventario').add({
            'name': name,
            'stock': int(stock),
            'price': float(price),
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        st.success(f"Producto '{name}' agregado con ID: {doc_ref[1].id}")
        return True
    except Exception as e:
        st.error(f"Error al agregar el producto: {e}")
        return False

# --- Interfaz de Usuario Streamlit ---

st.set_page_config(layout="wide") # Para un diseño más amplio si lo necesitas

st.title("📦 Gestión de Inventario en la Nube con Firestore")
st.subheader("Controla tus productos de manera eficiente.")

# --- Sección para Agregar Productos ---
st.header("➕ Agregar Nuevo Producto")
with st.form("add_product_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        product_name = st.text_input("Nombre del Producto", key="product_name_input")
    with col2:
        product_stock = st.number_input("Stock", min_value=0, step=1, key="product_stock_input")
    with col3:
        product_price = st.number_input("Precio Unitario", min_value=0.0, format="%.2f", key="product_price_input")

    submitted = st.form_submit_button("Agregar Producto")
    if submitted:
        if product_name and product_stock >= 0 and product_price >= 0:
            add_product(product_name, product_stock, product_price)
            # Recargar para mostrar el producto añadido
        else:
            st.warning("Por favor, rellena todos los campos correctamente.")

st.markdown("---") # Separador visual

# --- Sección para Mostrar Productos ---
st.header("📊 Productos Almacenados")

products = get_products()

if products:
    df_products = pd.DataFrame(products)
    # Reordenar columnas para una mejor visualización
    df_products = df_products[['name', 'stock', 'price', 'id', 'timestamp']]
    df_products.columns = ['Nombre', 'Stock', 'Precio', 'ID del Documento', 'Fecha de Creación'] # Renombrar columnas para la UI

    st.dataframe(df_products, use_container_width=True)

    # --- Sección de Resumen del Inventario ---
    st.header("📈 Resumen del Inventario")
    total_products = len(df_products)
    total_stock = df_products['Stock'].sum()
    total_value = (df_products['Stock'] * df_products['Precio']).sum()

    col_summary1, col_summary2, col_summary3 = st.columns(3)
    with col_summary1:
        st.metric(label="Total de Productos Diferentes", value=total_products)
    with col_summary2:
        st.metric(label="Stock Total de Unidades", value=f"{total_stock:,}")
    with col_summary3:
        st.metric(label="Valor Total del Inventario", value=f"${total_value:,.2f}")
else:
    st.info("No hay productos almacenados en Firestore. ¡Agrega uno usando el formulario de arriba!")
