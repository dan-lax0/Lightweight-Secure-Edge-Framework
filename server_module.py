from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding, hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization
import base64
from audit_logger import log_event


def load_files():
    with open("encrypted_data.bin", "rb") as f:
        ciphertext = f.read()

    with open("iv.bin", "rb") as f:
        iv = f.read()

    with open("hmac.txt", "r") as f:
        received_hmac = base64.b64decode(f.read())

    with open("encrypted_aes_key.bin", "rb") as f:
        encrypted_aes_key = f.read()

    return ciphertext, iv, received_hmac, encrypted_aes_key


def decrypt_aes_key(encrypted_aes_key):
    with open("server_private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    aes_key = private_key.decrypt(
        encrypted_aes_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return aes_key


def verify_hmac(aes_key, ciphertext, received_hmac):
    h = hmac.HMAC(aes_key, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    h.verify(received_hmac)


def decrypt_data(aes_key, iv, ciphertext):
    cipher = Cipher(
        algorithms.AES(aes_key),
        modes.CBC(iv),
        backend=default_backend()
    )

    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = sym_padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode()


if __name__ == "__main__":
    try:
        ciphertext, iv, received_hmac, encrypted_aes_key = load_files()

        # Step 1: Decrypt AES key using RSA
        aes_key = decrypt_aes_key(encrypted_aes_key)
        log_event("RSA_KEY_DECRYPTION", "SUCCESS", "AES key decrypted successfully")

        # Step 2: Verify HMAC
        verify_hmac(aes_key, ciphertext, received_hmac)
        log_event("HMAC_VERIFICATION", "SUCCESS", "Integrity verified successfully")

        # Step 3: Decrypt data
        plaintext = decrypt_data(aes_key, iv, ciphertext)
        log_event("DECRYPTION", "SUCCESS", "Data decrypted successfully")

        print("\nDecrypted Data:\n")
        print(plaintext)

    except Exception as e:
        log_event("SERVER_PROCESS", "FAILED", str(e))
        print("Integrity Verification Failed!")
        print("Error:", str(e))



