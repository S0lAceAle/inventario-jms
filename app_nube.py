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

# ---------------- 1. LISTA PRINCIPAL ----------------
st.subheader("📦 Productos en inventario")

products = get_products()

if not products:
    st.warning("No hay productos en Firebase")
else:
    st.success(f"Total productos: {len(products)}")

# ---------------- 2. BUSCADOR ----------------
st.subheader("🔍 Buscar producto")

search = st.text_input("Escribe el nombre")

if search:
    products = [
        p for p in products
        if search.lower() in p.get("name", "").lower()
    ]

# ---------------- 3. MOSTRAR + EDITAR + ELIMINAR ----------------
for p in products:
    st.markdown("---")

    st.write(f"**Nombre:** {p.get('name')}")
    st.write(f"Stock: {p.get('stock')}")
    st.write(f"Precio: {p.get('price')}")

    col1, col2 = st.columns(2)

    # ---------------- EDITAR ----------------
    with col1:
        with st.expander("✏️ Editar producto"):
            new_name = st.text_input("Nombre", value=p.get("name"), key=f"name_{p['id']}")
            new_stock = st.number_input("Stock", value=p.get("stock"), key=f"stock_{p['id']}")
            new_price = st.number_input("Precio", value=p.get("price"), key=f"price_{p['id']}")

            if st.button("Guardar cambios", key=f"save_{p['id']}"):
                update_product(p["id"], new_name, new_stock, new_price)
                st.success("Actualizado")
                st.rerun()

    # ---------------- ELIMINAR CON CONFIRMACIÓN ----------------
    with col2:
        if f"confirm_{p['id']}" not in st.session_state:
            st.session_state[f"confirm_{p['id']}"] = False

        if not st.session_state[f"confirm_{p['id']}"]:
            if st.button("🗑️ Eliminar", key=f"del_{p['id']}"):
                st.session_state[f"confirm_{p['id']}"] = True
                st.warning("Confirma eliminación")

        else:
            st.error("¿Seguro?")

            c1, c2 = st.columns(2)

            with c1:
                if st.button("Sí eliminar", key=f"yes_{p['id']}"):
                    delete_product(p["id"])
                    st.success("Eliminado")
                    st.rerun()

            with c2:
                if st.button("Cancelar", key=f"no_{p['id']}"):
                    st.session_state[f"confirm_{p['id']}"] = False
                    st.rerun()

# ---------------- 4. AGREGAR PRODUCTO ----------------
st.markdown("---")
st.subheader("➕ Agregar nuevo producto")

with st.form("add_form"):
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
