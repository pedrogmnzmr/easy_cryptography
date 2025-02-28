import streamlit as st
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BASE_DIR = "archivos"
CIFRADO_PATH = os.path.join(BASE_DIR, "cifrado.txt")
DESCIFRADO_PATH = os.path.join(BASE_DIR, "descifrado.txt")
os.makedirs(BASE_DIR, exist_ok=True)

# Inicializar clave y nonce en sesión
if "clave_nonce" not in st.session_state:
    st.session_state.clave_nonce = {"clave": get_random_bytes(16), "nonce": None}

def cifrar_texto(texto):
    cipher = AES.new(st.session_state.clave_nonce["clave"], AES.MODE_EAX)
    cifrado, _ = cipher.encrypt_and_digest(texto.encode("utf-8"))
    st.session_state.clave_nonce["nonce"] = cipher.nonce
    # guardar cifrado en binario
    with open(CIFRADO_PATH, "wb") as f:
        f.write(cifrado)
    return cifrado

def descifrar_texto():
    try:
        with open(CIFRADO_PATH, "rb") as f:
            cifrado = f.read()
        cipher = AES.new(
            st.session_state.clave_nonce["clave"],
            AES.MODE_EAX,
            nonce=st.session_state.clave_nonce["nonce"]
        )
        descifrado = cipher.decrypt(cifrado).decode("utf-8")
        with open(DESCIFRADO_PATH, "w", encoding="utf-8") as f:
            f.write(descifrado)
        return descifrado
    except Exception as e:
        return f"Error: {str(e)}"

st.title("Cifrado AES - PyCryptodome")

# tipo entrada
modo = st.radio("Selecciona la entrada:", ["Introducir manualmente", "Subir un archivo"])
texto = ""
archivo_subido = None

if modo == "Introducir manualmente":
    texto = st.text_area("Introduce el texto a cifrar:")
else:
    archivo = st.file_uploader("Sube un archivo TXT (texto o cifrado)", type=["txt"])
    if archivo:
        contenido = archivo.read()  # Leer en binario
        try:
            # Intentar decodificar como texto
            texto = contenido.decode("utf-8")
            st.text_area("Contenido del archivo:", texto, height=200)
        except UnicodeDecodeError:
            st.warning("Archivo cifrado detectado. Se guardará para descifrado.")
            with open(CIFRADO_PATH, "wb") as f:
                f.write(contenido)
            texto = ""  # no se cifra si se subio un cifrado

if st.button("Cifrar Texto") and texto:
    cifrado = cifrar_texto(texto)
    st.success("Texto cifrado y guardado en 'cifrado.txt'.")
    st.text_area("Texto Cifrado (bytes):", str(cifrado), height=150)

if st.button("Descifrar Texto"):
    descifrado = descifrar_texto()
    if descifrado.startswith("Error"):
        st.error(descifrado)
    else:
        st.success("Texto descifrado y guardado en 'descifrado.txt'.")
        st.text_area("Texto Descifrado:", descifrado, height=150)
