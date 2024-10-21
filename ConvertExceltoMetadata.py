import streamlit as st
import pandas as pd
from cryptography.fernet import Fernet
import pyperclip

# Generate kunci enkripsi (tetap untuk sesi ini)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Fungsi untuk enkripsi data
def encrypt_column(df, columns_to_encrypt):
    for col in columns_to_encrypt:
        df[col] = df[col].apply(lambda x: cipher_suite.encrypt(str(x).encode()).decode())
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

    # File upload
    uploaded_file = st.file_uploader("Unggah file CSV atau Excel", type=['csv', 'xlsx'])

    if uploaded_file is not None:
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
            df = encrypt_column(df, columns_to_encrypt)

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
