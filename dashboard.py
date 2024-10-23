import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
API_KEY = os.getenv("AZURE_API_KEY_MODEL_4o")

# Fungsi untuk mengubah format data chat
def format_chat_data(row):
    return f"Waktu: {row['Waktu']}, User: {row['User']}, Pertanyaan: {row['Pertanyaan']}, Jawaban: {row['Jawaban']}"

# Judul aplikasi
st.title("Dashboard Chat Log")

# Membaca file Excel
chat_log_file = "chat_log.xlsx"

# Endpoint Azure OpenAI
ENDPOINT = "https://squad2new.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"  # Ganti dengan API key Anda
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

try:
    # Load data dari file Excel
    data = pd.read_excel(chat_log_file)

    # Format data menjadi string sesuai kebutuhan
    formatted_data = data.apply(format_chat_data, axis=1).tolist()

    # Menampilkan data dalam format yang diinginkan
    st.subheader("Data Chat:")
    DataChat = ""
    for chat in formatted_data:
        DataChat += chat + "\n"
    
    st.text_area("Data Chat", DataChat, height=300)
    
    # Mengirim data ke endpoint Azure untuk mendapatkan insight
    prompt = """
            Analisis Pengguna
            Tugas:
                1. Identifikasi jenis pertanyaan yang sering diajukan oleh user dan kategori pertanyaan tersebut (misalnya, informasi akun, fitur aplikasi, dll.).
                2. Analisis respons yang disukai user, seperti gaya percakapan (formal/informal, penggunaan kata-kata santai, dsb.) dan elemen yang membuatnya merasa terhubung dengan chatbot.
                3. Catat pola dalam frekuensi interaksi, seperti waktu dan konteks di mana user cenderung aktif.
                4. Berikan rekomendasi untuk meningkatkan pengalaman pengguna berdasarkan preferensi dan pola yang ditemukan, termasuk cara menyesuaikan gaya percakapan dan meningkatkan relevansi informasi yang disediakan.
                5. Buat kesimpulan dari analisis yang dilakukan dan sertakan rekomendasi yang spesifik dan terukur.
                6. Berdasarkan log obrolan di atas, apa yang dapat Anda simpulkan tentang pengguna? Memberikan wawasan tentang preferensi, perilaku, dan informasi lain yang relevan dengan pengguna.
            """
    
    # Membuat payload untuk permintaan
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information."
        }
    ]

    # Menambahkan chat yang sudah diformat ke dalam payload
    for chat in formatted_data:
        messages.append({
            "role": "user",
            "content": chat
        })
    
    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    # Kirim permintaan ke Azure OpenAI
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    
    # Menampilkan insight dari respons
    st.subheader("Insight:")
    insights = response.json()
    if 'choices' in insights and len(insights['choices']) > 0:
        insights_content = insights['choices'][0]['message']['content']
    else:
        insights_content = "Tidak ada insight yang diterima."
    
    st.write(insights_content)

except FileNotFoundError:
    st.error("File chat_log.xlsx tidak ditemukan.")
except requests.HTTPError as http_err:
    st.error(f"HTTP error occurred: {http_err}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {str(e)}")
