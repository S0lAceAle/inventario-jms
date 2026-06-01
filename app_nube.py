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
    except Exception as e:
        st.error("Error conectando Firebase")
        st.error(e)

db = firestore.client()

# ---------------- AGREGAR ----------------
st.subheader("➕ Agregar producto")

with st.form("add"):
    name = st.text_input("Nombre")
    stock = st.number_input("Stock", min_value=0, step=1)
    price = st.number_input("Precio", min_value=0.0, format="%.2f")

    if st.form_submit_button("Agregar"):
        db.collection("inventario").add({
            "name": name,
            "stock": int(stock),
            "price": float(price)
        })
        st.success("Producto agregado")
        st.rerun()

# ---------------- OBTENER ----------------
def get_products():
    docs = db.collection("inventario").stream()
    products = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        products.append(data)

    return products

# ---------------- ACCIONES ----------------
def delete_product(pid):
    db.collection("inventario").document(pid).delete()

def update_product(pid, name, stock, price):
    db.collection("inventario").document(pid).update({
        "name": name,
        "stock": int(stock),
        "price": float(price)
    })

# ---------------- BUSCADOR ----------------
st.subheader("🔍 Buscar producto")

search = st.text_input("Escribe nombre para buscar")

products = get_products()

if search:
    products = [
        p for p in products
        if search.lower() in p.get("name", "").lower()
    ]

# ---------------- MOSTRAR ----------------
st.subheader("📦 Productos")

for p in products:
    st.markdown("---")

    st.write("**Nombre:**", p.get("name"))
    st.write("Stock:", p.get("stock"))
    st.write("Precio:", p.get("price"))

    col1, col2 = st.columns(2)

    # EDITAR
    with col1:
        with st.expander("✏️ Editar"):
            new_name = st.text_input("Nombre", p.get("name"), key=f"n{p['id']}")
            new_stock = st.number_input("Stock", value=p.get("stock"), key=f"s{p['id']}")
            new_price = st.number_input("Precio", value=p.get("price"), key=f"p{p['id']}")

            if st.button("Guardar", key=f"save{p['id']}"):
                update_product(p["id"], new_name, new_stock, new_price)
                st.rerun()

    # ELIMINAR
    with col2:
        if st.button("🗑️ Eliminar", key=f"d{p['id']}"):
            delete_product(p["id"])
            st.rerun()
