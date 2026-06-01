import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Inventario en la Nube", layout="wide")

st.title("☁️ Inventario en la Nube (Firebase)")

st.write("Conectando a Firebase...")

# ---------------- FIREBASE INIT ----------------
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
        st.success("Firebase conectado correctamente")
    except Exception as e:
        st.error("Error conectando Firebase")
        st.error(e)

db = firestore.client()

# ---------------- OBTENER PRODUCTOS ----------------
def get_products():
    try:
        docs = db.collection("inventario").stream()

        products = []

        for doc in docs:
            data = doc.to_dict()

            # 🔥 normalización para evitar errores de campos
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
st.header("📦 Productos en la nube")

products = get_products()

if len(products) > 0:
    st.dataframe(products, use_container_width=True)
else:
    st.warning("No se encontraron productos en Firestore")