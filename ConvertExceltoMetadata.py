import streamlit as st
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
import base64
import pyperclip

# Fungsi untuk menghasilkan kunci dari password (deterministik)
def get_key(password):
    salt = b'static_salt'  # Salt statis untuk konsistensi (tidak disarankan dalam situasi nyata)
    key = PBKDF2(password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
    return key

# Fungsi untuk mengenkripsi data secara deterministik
def encrypt_deterministic(data, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = data.ljust(32)  # Padding agar panjang data pas untuk blok AES (32 byte)
    encrypted_data = cipher.encrypt(padded_data.encode())
    return base64.b64encode(encrypted_data).decode()

# Fungsi untuk mendekripsi data
def decrypt_deterministic(encrypted_data, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_ECB)
    decoded_encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_encrypted_data)
    return decrypted_data.decode().strip()  # Menghapus padding

# Fungsi untuk enkripsi data dalam kolom
def encrypt_column(df, columns_to_encrypt, password):
    for col in columns_to_encrypt:
        df[col] = df[col].apply(lambda x: encrypt_deterministic(str(x), password))
    return df

# Fungsi untuk mengubah format data secara dinamis
def format_data(df, selected_columns):
    formatted_data = []
    for index, row in df.iterrows():
        formatted_row = ', '.join([f"{col} : {row[col]}" for col in selected_columns])
        formatted_data.append(formatted_row)
    return formatted_data

# Fungsi untuk menyalin data ke clipboard
def copy_to_clipboard(formatted_data):
    formatted_text = "\n".join(formatted_data)
    pyperclip.copy(formatted_text)

# Fungsi utama untuk Streamlit
def main():
    st.title('MetaData Index Converter')

    # Password untuk enkripsi
    st.text("Password untuk Enkripsi: 1234")
    password = st.text_input("Masukkan Password untuk Enkripsi", type="password")

    # File upload
    uploaded_file = st.file_uploader("Unggah file CSV atau Excel", type=['csv', 'xlsx'])

    if uploaded_file is not None and password:
        # Memuat file ke dataframe
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("Data Awal:")
        st.dataframe(df)

        # Pemilihan kolom untuk digunakan
        selected_columns = st.multiselect(
            "Pilih Kolom yang Akan Digunakan",
            options=df.columns,
            default=df.columns.tolist()
        )

        # Pemilihan kolom untuk dienkripsi
        columns_to_encrypt = st.multiselect(
            "Pilih Kolom yang Akan Dienkripsi",
            options=selected_columns,
            help="Hanya kolom yang dipilih sebelumnya bisa dienkripsi"
        )

        # Jika ada kolom yang dipilih untuk dienkripsi, lakukan enkripsi
        if columns_to_encrypt:
            df = encrypt_column(df, columns_to_encrypt, password)

        # Mengubah format data berdasarkan kolom yang dipilih
        formatted_data = format_data(df, selected_columns)

        # Menampilkan hasil format baru dalam kotak dengan scroll bar
        st.write("Data Setelah Diubah:")
        formatted_text = '\n'.join(formatted_data)
        st.text_area("Hasil Format", formatted_text, height=300)

        # Tombol untuk menyalin ke clipboard
        if st.button("Salin ke Clipboard"):
            copy_to_clipboard(formatted_data)
            st.success("Data berhasil disalin ke clipboard!")

# Menjalankan aplikasi
if __name__ == '__main__':
    main()
