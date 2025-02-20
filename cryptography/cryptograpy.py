from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

clave = os.urandom(16) 
iv = os.urandom(16)  

texto = input("Introduce un texto para cifrar: ")

if not os.path.exists("archivos"):
    os.makedirs("archivos")

# cifra el mensaje
mensaje = texto.encode()
mensaje += b' ' * (16 - len(mensaje) % 16)
cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
cifrado = encryptor.update(mensaje) + encryptor.finalize()

print("-----------------------------------")
print("Mensaje a Cifrar:", texto)
print("-----------------------------------")
print("Texto Cifrado:", cifrado)

# guardar mensaje cifrado
with open("archivos/cifrado.txt", "wb") as file:
    file.write(cifrado)

# descifra mensaje
cipher_dec = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
decryptor = cipher_dec.decryptor()
mensaje_descifrado = decryptor.update(cifrado) + decryptor.finalize()
mensaje_descifrado = mensaje_descifrado.rstrip().decode()

print("Texto Descifrado:", mensaje_descifrado)

# guardar mensaje descifrado
with open("archivos/descifrado.txt", "w") as file:
    file.write(mensaje_descifrado)
