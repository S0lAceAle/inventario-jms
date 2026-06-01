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
st.subheader("➕ Agregar producto")

with st.form("add_form"):
    name = st.text_input("Nombre")
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
            st.success("Producto agregado")
            st.rerun()
        else:
            st.warning("Escribe un nombre")

# ---------------- FUNCION OBTENER ----------------
def get_products():
    docs = db.collection("inventario").stream()

    products = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        products.append(data)

    return products

# ---------------- ELIMINAR ----------------
def delete_product(product_id):
    db.collection("inventario").document(product_id).delete()

# ---------------- EDITAR ----------------
def update_product(product_id, name, stock, price):
    db.collection("inventario").document(product_id).update({
        "name": name,
        "stock": int(stock),
        "price": float(price)
    })

# ---------------- UI ----------------
st.subheader("📦 Productos")

products = get_products()

for p in products:
    with st.container():
        st.markdown("---")

        st.write(f"**Nombre:** {p.get('name')}")
        st.write(f"Stock: {p.get('stock')}")
        st.write(f"Precio: {p.get('price')}")

        col1, col2, col3 = st.columns(3)

        # ---------------- EDITAR ----------------
        with col1:
            with st.expander("✏️ Editar"):
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
                st.error("¿Seguro que quieres eliminar?")
                col_a, col_b = st.columns(2)

                with col_a:
                    if st.button("Sí, eliminar", key=f"yes_{p['id']}"):
                        delete_product(p["id"])
                        st.success("Eliminado")
                        st.rerun()

                with col_b:
                    if st.button("Cancelar", key=f"no_{p['id']}"):
                        st.session_state[f"confirm_{p['id']}"] = False
                        st.rerun()

        with col3:
            st.info("Gestión de producto")
