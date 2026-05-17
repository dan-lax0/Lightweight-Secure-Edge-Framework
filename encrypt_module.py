from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding, hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization
import os
import base64
from audit_logger import log_event
import time


def read_edge_data():
    with open("edge_data.txt", "r") as file:        return file.read()


def encrypt_data(data):
    aes_key = os.urandom(32)
    iv = os.urandom(16)

    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(aes_key),
        modes.CBC(iv),
        backend=default_backend()
    )

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return aes_key, iv, ciphertext


def generate_hmac(aes_key, ciphertext):
    h = hmac.HMAC(aes_key, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    return h.finalize()


def save_outputs(iv, ciphertext, hmac_value, encrypted_aes_key):
    with open("encrypted_data.bin", "wb") as f:
        f.write(ciphertext)

    with open("iv.bin", "wb") as f:
        f.write(iv)

    with open("hmac.txt", "w") as f:
        f.write(base64.b64encode(hmac_value).decode())

    with open("encrypted_aes_key.bin", "wb") as f:
        f.write(encrypted_aes_key)


if __name__ == "__main__":
    try:
        start = time.time()

        data = read_edge_data()
        log_event("READ_EDGE_DATA", "SUCCESS", "Edge data read successfully")

        aes_key, iv, ciphertext = encrypt_data(data)
        log_event("ENCRYPTION", "SUCCESS", "Data encrypted using AES-256")

        hmac_value = generate_hmac(aes_key, ciphertext)
        log_event("HMAC_GENERATION", "SUCCESS", "HMAC-SHA256 generated")

        # Load Server Public Key
        with open("server_public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        # Encrypt AES key using RSA
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        log_event("RSA_KEY_ENCRYPTION", "SUCCESS", "AES key encrypted using RSA")

        save_outputs(iv, ciphertext, hmac_value, encrypted_aes_key)
        log_event("SAVE_ENCRYPTED_OUTPUT", "SUCCESS", "Encrypted files saved successfully")

        end = time.time()  # ✅ END HERE
        print(f"Encryption Time: {end - start:.4f} seconds")

        print("Hybrid Encryption completed successfully!")

    except Exception as e:
        log_event("ENCRYPTION_PROCESS", "FAILED", str(e))
        print("Encryption failed:", str(e))