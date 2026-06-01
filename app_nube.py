import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Inventario en la Nube", layout="wide")

st.title("☁️ Inventario en la Nube (Firebase)")

# ---------------- FIREBASE INIT ----------------
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(st.secrets["firebase"])
        firebase_admin.initialize_app(cred)
        st.success("Firebase conectado correctamente")
    except Exception as e:
        st.error("Error conectando Firebase")
        st.error(e)

db = firestore.client()

# ---------------- AGREGAR PRODUCTO ----------------
st.subheader("➕ Agregar producto en tiempo real")

with st.form("form_add"):
    name = st.text_input("Nombre del producto")
    stock = st.number_input("Stock", min_value=0, step=1)
    price = st.number_input("Precio", min_value=0.0, format="%.2f")

    submit = st.form_submit_button("Agregar")

    if submit:
        if name:
            db.collection("inventario").add({
                "name": name,
                "stock": int(stock),
                "price": float(price)
            })
            st.success("Producto agregado correctamente")
            st.rerun()
        else:
            st.warning("Escribe un nombre")

# ---------------- OBTENER PRODUCTOS ----------------
def get_products():
    try:
        docs = db.collection("inventario").stream()

        products = []

        for doc in docs:
            data = doc.to_dict()

            products.append({
                "Nombre": data.get("name", "Sin nombre"),
                "Stock": data.get("stock", 0),
                "Precio": data.get("price", 0),
                "ID": doc.id
            })

        return products

    except Exception as e:
        st.error("Error leyendo Firestore")
        st.error(e)
        return []

# ---------------- UI ----------------
st.subheader("📦 Productos en la nube")

products = get_products()

if products:
    st.dataframe(products, use_container_width=True)
    st.success(f"Total productos: {len(products)}")
else:
    st.warning("No hay productos en Firestore")