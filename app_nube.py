import streamlit as st
import pandas as pd
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

# ---------------- DATA ----------------
def get_products():
    docs = db.collection("inventario").stream()
    data = []

    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        data.append(d)

    return data

def delete_product(pid):
    db.collection("inventario").document(pid).delete()

def update_product(pid, name, stock, price):
    db.collection("inventario").document(pid).update({
        "name": name,
        "stock": int(stock),
        "price": float(price)
    })

# ---------------- AGREGAR ----------------
st.subheader("➕ Agregar producto")

with st.form("add"):
    name = st.text_input("Nombre")
    stock = st.number_input("Stock", min_value=0)
    price = st.number_input("Precio", min_value=0.0)

    if st.form_submit_button("Agregar"):
        db.collection("inventario").add({
            "name": name,
            "stock": int(stock),
            "price": float(price)
        })
        st.success("Agregado")
        st.rerun()

# ---------------- BUSCAR ----------------
st.subheader("🔍 Buscar")

search = st.text_input("Buscar producto")

products = get_products()

if search:
    products = [p for p in products if search.lower() in p.get("name","").lower()]

# ---------------- TABLA ----------------
st.subheader("📊 Inventario (Tabla)")

if products:
    df = pd.DataFrame(products)
    df = df[["name", "stock", "price", "id"]]
    df.columns = ["Nombre", "Stock", "Precio", "ID"]

    st.dataframe(df, use_container_width=True)
else:
    st.warning("No hay productos")

# ---------------- CRUD ----------------
st.subheader("✏️ Editar / 🗑️ Eliminar")

for p in products:
    st.markdown("---")

    col1, col2 = st.columns(2)

    # EDITAR
    with col1:
        with st.expander(f"Editar {p['name']}"):
            new_name = st.text_input("Nombre", p.get("name"), key=f"n{p['id']}")
            new_stock = st.number_input("Stock", p.get("stock"), key=f"s{p['id']}")
            new_price = st.number_input("Precio", p.get("price"), key=f"p{p['id']}")

            if st.button("Guardar", key=f"save{p['id']}"):
                update_product(p["id"], new_name, new_stock, new_price)
                st.rerun()

    # ELIMINAR CON CONFIRMACIÓN
    with col2:
        if f"conf_{p['id']}" not in st.session_state:
            st.session_state[f"conf_{p['id']}"] = False

        if not st.session_state[f"conf_{p['id']}"]:
            if st.button("🗑️ Eliminar", key=f"del{p['id']}"):
                st.session_state[f"conf_{p['id']}"] = True
                st.warning("Confirma eliminación")

        else:
            st.error("¿Seguro?")

            c1, c2 = st.columns(2)

            with c1:
                if st.button("Sí", key=f"yes{p['id']}"):
                    delete_product(p["id"])
                    st.rerun()

            with c2:
                if st.button("No", key=f"no{p['id']}"):
                    st.session_state[f"conf_{p['id']}"] = False
                    st.rerun()
