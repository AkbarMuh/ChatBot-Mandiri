import streamlit as st

# Simulasi database user
users = {
    "user1": "1234",
    "user2": "1234",
}

# Fungsi untuk login
def login(username, password):
    if username in users and users[username] == password:
        return True
    return False

# Fungsi untuk menampilkan chat
def chat(username):
    st.title("Sistem Chat")

    # Menyimpan pesan dalam session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Tampilkan pesan sambutan
    st.write("Selamat datang " + username + "! Silakan tulis pesan Anda.")

    # Input pesan
    message = st.text_input("Tulis pesan:", "")

    # Tombol kirim
    if st.button("Kirim"):
        if message:
            st.session_state.messages.append(message)
            # Reset input setelah kirim
            st.session_state.new_message = ""  

    # Menampilkan pesan
    st.subheader("Pesan:")
    for msg in st.session_state.messages:
        st.write(f"- {msg}")

    # Tombol Logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.messages = []  # Reset pesan saat logout
        st.success("Anda telah logout.")
        st.experimental_rerun()  # Memaksa Streamlit untuk merender ulang

# Judul aplikasi
st.title("Sistem Login Sederhana")

# Form untuk login
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    with st.form(key='login_form'):
        username = st.selectbox("Pilih Username", options=list(users.keys()))  # Dropdown untuk username
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

    # Memeriksa login
    if submit_button:
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username  # Menyimpan username dalam session state
            st.experimental_rerun()  # Memaksa Streamlit untuk merender ulang
        else:
            st.error("Username atau password salah.")
else:
    # Jika sudah login, tampilkan sistem chat
    chat(st.session_state.username)
