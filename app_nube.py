import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Inventario en la Nube", layout="wide")

st.title("☁️ Inventario en la Nube (Firebase)")

st.write("Conectando a Firestore...")

# ---------------- FIREBASE INIT ----------------
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        st.success("Firebase conectado correctamente")
    except Exception as e:
        st.error(f"Error conectando Firebase: {e}")

db = firestore.client()

# ---------------- GET DATA ----------------
def get_products():
    try:
        docs = db.collection("inventario").stream()

        products = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            products.append(data)

        return products

    except Exception as e:
        st.error(f"Error leyendo Firestore: {e}")
        return []

# ---------------- UI ----------------
st.header("📦 Productos en la nube")

products = get_products()

if products:
    st.dataframe(products, use_container_width=True)
else:
    st.warning("No hay productos en Firestore o no se pudieron cargar.")