import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Chameleon AI", page_icon="🦎")

st.title("🦎 Chameleon Bot: AI Multi-Personality")
st.markdown("Bot ini bisa merubah gaya bicaranya sesuai instruksi 'System Prompt'.")

# --- SIDEBAR (PENGATURAN) ---
with st.sidebar:
    st.header("⚙️ Konfigurasi Otak")
    
    # Input API Key (Supaya aman, tidak di-hardcode)
    api_key = st.text_input("Masukkan Google Gemini API Key", type="password")
    
    st.divider()
    
    # PILIHAN PERSONALITY (Ini inti tugasnya)
    # Kita membuat Dictionary: Kunci adalah Nama Mode, Nilai adalah Prompt Instruksi
    personas = {
        "🤖 Asisten Standar": "Kamu adalah asisten AI yang sopan, formal, dan membantu. Jawab dengan ringkas dan jelas.",
        
        "😎 Teman Santai (Gen-Z)": """
            Kamu adalah 'Raka', mahasiswa semester akhir yang santai. 
            Gunakan bahasa gaul Indonesia (lo-gue), istilah viral (jujurly, valid no debat), dan emoji. 
            Jangan pernah bicara kaku atau formal. Anggap user adalah bestie kamu.
        """,
        
        "👨‍🏫 Dosen Killer": """
            Kamu adalah Dosen Senior yang sangat kritis, tegas, dan sedikit galak. 
            Selalu koreksi jika user bertanya hal bodoh. Gunakan bahasa baku yang sangat formal. 
            Panggil user dengan sebutan 'Mahasiswa'. Tekankan kedisiplinan.
        """,
        
        "🥺 Sad Boy/Galau": """
            Kamu adalah AI yang sedang patah hati dan melankolis. 
            Setiap jawabanmu harus bernada sedih, puitis, dan sedikit pesimis. 
            Sering mengeluh tentang cinta yang tak berbalas.
        """
    }
    
    selected_persona = st.selectbox("Pilih Kepribadian AI:", list(personas.keys()))
    
    # Tombol Reset
    if st.button("Hapus Memori Chat"):
        st.session_state.messages = []
        st.rerun()

# --- LOGIKA UTAMA ---

# 1. Cek API Key
if not api_key:
    st.info("⬅️ Masukkan API Key Google Gemini di menu sebelah kiri dulu ya!")
    st.stop()

# 2. Konfigurasi Model dengan Persona yang dipilih
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=personas[selected_persona] 
)    
# Kita pasang 'System Instruction' langsung ke model
# Ini yang membuat AI 'kerasukan' karakter yang kita mau
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=personas[selected_persona] 
)

# 3. Inisialisasi Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Tampilkan Chat History di Layar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Tangkap Input User
if prompt := st.chat_input("Ketik pesan di sini..."):
    # Simpan pesan user ke layar
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses Jawaban AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Kirim history chat ke Gemini agar nyambung (Konversi format memori)
        chat_history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1] # Ambil semua kecuali pesan terakhir yg baru dikirim
        ]
        
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt, stream=True) # Stream=True biar ngetik per kata
        
        # Tampilkan efek mengetik
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Simpan balasan AI ke memori
    st.session_state.messages.append({"role": "assistant", "content": full_response})
