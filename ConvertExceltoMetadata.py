import streamlit as st
import pandas as pd
import pyperclip

# Fungsi Caesar cipher untuk encoding
def caesar_cipher(text, shift):
    encoded_text = ""
    for char in text:
        if char.isalpha():  # Hanya menggeser huruf
            shift_base = ord('A') if char.isupper() else ord('a')
            encoded_text += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encoded_text += char  # Non-huruf tetap sama
    return encoded_text

# Fungsi untuk encode data dalam kolom menggunakan Caesar cipher dengan separator '| |'
def encode_column(df, columns_to_encode, shift):
    for col in columns_to_encode:
        df[col] = df[col].astype(str).apply(lambda x: '|-' + caesar_cipher(x, shift) + '-|')
    return df

# Fungsi untuk mengubah format data secara dinamis
def format_data(df, selected_columns):
    return [', '.join([f"{col} : {row[col]}" for col in selected_columns]) for _, row in df.iterrows()]

# Fungsi untuk menyalin data ke clipboard
def copy_to_clipboard(formatted_data):
    formatted_text = "\n".join(formatted_data)
    pyperclip.copy(formatted_text)

# Fungsi utama untuk Streamlit
def main():
    st.title('MetaData Index Converter - Caesar Cipher')

    # Nilai shift untuk Caesar cipher
    shift = st.number_input("Masukkan nilai shift untuk encoding Caesar", min_value=1, max_value=25, value=3)

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

        # Pemilihan kolom untuk di-encode
        columns_to_encode = st.multiselect(
            "Pilih Kolom yang Akan Di-encode",
            options=selected_columns,
            help="Hanya kolom yang dipilih sebelumnya bisa di-encode"
        )

        # Jika ada kolom yang dipilih untuk di-encode, lakukan encoding
        if columns_to_encode:
            df = encode_column(df, columns_to_encode, shift)

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
