import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Conectar con Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Leer Excel
df = pd.read_excel("inventario accesorios JMS.xlsx")

# Limpiar nombres de columnas
df.columns = [str(col).strip().lower() for col in df.columns]

# Recorrer filas
for index, row in df.iterrows():

    producto = str(row["producto"]).strip()

    # Saltar filas vacías
    if producto == "" or producto.lower() == "nan":
        continue

    # Saltar categorías como FORROS, VIDRIOS, etc.
    if producto.isupper():
        continue

    try:
        stock = int(row["unidades"])
    except:
        stock = 0

    try:
        precio_texto = str(row["precio unitario ($)"])

        # Quitar símbolos y comas
        precio_texto = precio_texto.replace("$", "")
        precio_texto = precio_texto.replace(",", "")
        precio_texto = precio_texto.strip()

        precio = float(precio_texto)

    except:
        precio = 0

    db.collection("inventario").add({
        "name": producto,
        "stock": stock,
        "price": precio,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    print("Subido:", producto)

print("\n✅ Carga completada")