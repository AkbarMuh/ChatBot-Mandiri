from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
import base64

# Fungsi untuk menghasilkan kunci yang konsisten dari password
def get_key(password):
    salt = b'static_salt'  # Gunakan salt yang statis (tidak dianjurkan dalam situasi nyata)
    key = PBKDF2(password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
    return key

# Fungsi untuk mengenkripsi data secara deterministik
def encrypt_deterministic(data, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_ECB)  # Menggunakan mode ECB (Electronic Codebook) untuk menghasilkan ciphertext konsisten
    padded_data = data.ljust(32)  # Padding agar data pas untuk blok AES (16 atau 32 byte)
    encrypted_data = cipher.encrypt(padded_data.encode())
    return base64.b64encode(encrypted_data).decode()  # Menghasilkan ciphertext dalam format string base64

# Fungsi untuk mendekripsi data
def decrypt_deterministic(encrypted_data, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_ECB)
    decoded_encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_encrypted_data)
    return decrypted_data.decode().strip()  # Menghapus padding

# Contoh penggunaan
password = "1234"  # Kunci tetap untuk enkripsi
data = "Data penting"

print(f"Data Asli: {data}")

# Enkripsi
encrypted = encrypt_deterministic(data, password)
print(f"Encrypted: {encrypted}")

# Dekripsi
decrypted = decrypt_deterministic(encrypted, password)
print(f"Decrypted: {decrypted}")

print(encrypt_deterministic(data, "1234")==encrypted)