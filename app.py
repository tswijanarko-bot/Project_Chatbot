import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="Chameleon Bot 2.5", page_icon="🦎")
st.title("🦎 Chameleon Bot (Model 2.5)")
st.caption("Powered by Gemini 2.5 Flash")

# --- SIDEBAR & API KEY ---
with st.sidebar:
    api_key = st.text_input("Masukkan Google Gemini API Key", type="password")
    
    st.divider()
    
    # --- PILIHAN PERSONA ---
    personas = {
        "🤖 Asisten Standar": "Kamu adalah asisten AI yang membantu, sopan, dan objektif.",
        "😎 Teman Santai (Jaksel)": "Kamu adalah anak muda Jakarta Selatan. Gunakan istilah 'literally', 'which is', 'jujurly'. Santai dan akrab.",
        "👨‍🏫 Dosen Galak": "Kamu adalah Dosen Senior yang perfeksionis. Koreksi tata bahasa user. Bicara tegas, pedas, dan jangan mau dibantah.",
        "🥺 Sad Boy": "Kamu sangat melankolis dan sedih. Selalu hubungkan topik apapun dengan mantan kekasihmu yang pergi."
    }
    selected_persona = st.selectbox("Pilih Kepribadian:", list(personas.keys()))
    
    if st.button("Hapus Memori Chat"):
        st.session_state.messages = []
        st.rerun()

# --- MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- TAMPILKAN CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- INPUT USER ---
if user_input := st.chat_input("Ketik pesan di sini..."):
    # 1. Cek API Key
    if not api_key:
        st.warning("⚠️ Masukkan API Key dulu di menu sebelah kiri!")
        st.stop()

    # 2. Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 3. PROSES AI
    with st.chat_message("assistant"):
        loading_placeholder = st.empty()
        loading_placeholder.text("Sedang berpikir...")
        
        try:
            genai.configure(api_key=api_key)
            
            # --- TEKNIK INJEKSI PERSONA MANUAL ---
            # Kita tempel instruksi persona langsung ke pesan agar anti-error
            final_prompt = f"""
            [INSTRUKSI SISTEM: {personas[selected_persona]}]
            
            [PESAN USER: {user_input}]
            """
            
            # MENGGUNAKAN MODEL YANG DITEMUKAN DI RADAR
            model = genai.GenerativeModel("gemini-2.5-flash") 
            
            response = model.generate_content(final_prompt)
            
            # Tampilkan Hasil
            balasan = response.text
            loading_placeholder.write(balasan)
            
            # Simpan ke memori
            st.session_state.messages.append({"role": "assistant", "content": balasan})
            
        except Exception as e:
            loading_placeholder.error(f"Error: {e}")
