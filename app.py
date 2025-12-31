import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="Bot Tugas", page_icon="🤖")
st.title("🤖 Chatbot Tugas Kuliah")

# --- SIDEBAR & API KEY ---
api_key = st.sidebar.text_input("Masukkan Google Gemini API Key", type="password")

# --- PILIHAN PERSONA ---
personas = {
    "Asisten Biasa": "Jawab dengan sopan dan singkat.",
    "Teman Gaul": "Gunakan bahasa gaul Indonesia (lu-gue), santai, dan pakai emoji.",
    "Dosen Galak": "Gunakan bahasa formal, tegas, panggil user 'Mahasiswa', dan sedikit meremehkan."
}
pilihan = st.sidebar.selectbox("Pilih Gaya Bicara:", list(personas.keys()))

# --- MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- TAMPILKAN CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- INPUT USER ---
if user_input := st.chat_input("Ketik pesan..."):
    # 1. Cek API Key
    if not api_key:
        st.warning("⚠️ Masukkan API Key dulu di sebelah kiri!")
        st.stop()

    # 2. Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 3. LOGIKA MANUAL (ANTI-ERROR)
    try:
        genai.configure(api_key=api_key)
        
        # TRIK: Kita gabungkan instruksi ke dalam pesan user
        # Ini bypass kebutuhan fitur 'system_instruction' yang bikin error
        final_prompt = f"PERAN KAMU: {personas[pilihan]}\n\nUSER BERTANYA: {user_input}"
        
        # Kita pakai model 1.5 Flash. Jika gagal, kode akan otomatis lapor.
        model = genai.GenerativeModel("gemini-pro")
        
        # Matikan stream=True biar tidak ribet
        response = model.generate_content(final_prompt)
        
        # 4. Tampilkan Balasan
        balasan = response.text
        st.session_state.messages.append({"role": "assistant", "content": balasan})
        with st.chat_message("assistant"):
            st.write(balasan)
            
    except Exception as e:
        st.error(f"Terjadi Kesalahan: {e}")
        st.error("Coba ganti API Key atau Refresh halaman.")
