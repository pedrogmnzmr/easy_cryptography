import streamlit as st
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

BASE_DIR = "archivos"
CIFRADO_FILE = os.path.join(BASE_DIR, "cifrado.txt")
DESCIFRADO_FILE = os.path.join(BASE_DIR, "descifrado.txt")
os.makedirs(BASE_DIR, exist_ok=True)

# Inicializar clave e IV en sesión de Streamlit
if "aes_data" not in st.session_state:
    st.session_state.aes_data = {"clave": os.urandom(16), "iv": os.urandom(16)}

# aplica padding simple con ljust
def cifrar_texto(texto):
    mensaje = texto.encode().ljust(16 * ((len(texto) // 16) + 1))
    clave, iv = st.session_state.aes_data["clave"], st.session_state.aes_data["iv"]
    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
    cifrado = cipher.encryptor().update(mensaje) + cipher.encryptor().finalize()
    # guardar cifrado en binario
    with open(CIFRADO_FILE, "wb") as f:
        f.write(cifrado)
    return cifrado

# si el archivo ya es texto, se retorna directamente
def descifrar_texto(archivo_binario=None):
    try:
        # si se sube archivo usarlo sino lee archivo guardado
        data = archivo_binario if archivo_binario is not None else open(CIFRADO_FILE, "rb").read()

        # archivo puede decodificarse como UTF-8, se asume que ya está descifrado
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            # De lo contrario, se procede a descifrar
            clave, iv = st.session_state.aes_data["clave"], st.session_state.aes_data["iv"]
            cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
            descifrado = cipher.decryptor().update(data) + cipher.decryptor().finalize()
            descifrado = descifrado.rstrip().decode("utf-8")
            with open(DESCIFRADO_FILE, "w", encoding="utf-8") as f:
                f.write(descifrado)
            return descifrado
    except Exception as e:
        return f"Error: {str(e)}"

st.title("Cifrado AES - Cryptography")

# tipo entrada
modo = st.radio("Elige la entrada:", ["Introducir manualmente", "Subir un archivo"])
texto = ""
archivo_binario = None

if modo == "Introducir manualmente":
    texto = st.text_area("Introduce el texto a cifrar:")
else:
    archivo = st.file_uploader("Sube un archivo TXT (texto o cifrado)", type=["txt"])
    if archivo:
        archivo_binario = archivo.read()  # Leer en binario
        try:
            texto = archivo_binario.decode("utf-8")
            st.text_area("Contenido del archivo (texto):", texto, height=200)
        except UnicodeDecodeError:
            st.warning("Archivo cifrado detectado. Se usará para descifrado.")
            texto = "" # no se cifra si se subio un cifrado

if st.button("Cifrar Texto") and texto:
    cifrado = cifrar_texto(texto)
    st.success("Texto cifrado y guardado en 'cifrado.txt'.")
    st.text_area("Texto Cifrado (bytes):", str(cifrado), height=150)

if st.button("Descifrar Texto"):
    descifrado = descifrar_texto(archivo_binario)
    if descifrado.startswith("Error"):
        st.error(descifrado)
    else:
        st.success("Texto descifrado y guardado en 'descifrado.txt'.")
        st.text_area("Texto Descifrado:", descifrado, height=150)
