import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Chameleon AI", page_icon="🦎")
st.title("🦎 Chameleon Bot: Versi Aman")

api_key = st.sidebar.text_input("Masukkan Google Gemini API Key", type="password")

# Persona Manual (Tanpa System Instruction Canggih)
personas = {
    "🤖 Asisten Standar": "Kamu adalah asisten AI yang sopan.",
    "😎 Teman Santai": "Kamu adalah Raka, bicara lu-gue dan santai.",
    "👨‍🏫 Dosen Killer": "Kamu adalah Dosen galak, bicara formal dan tegas."
}
selected_persona = st.sidebar.selectbox("Pilih Kepribadian:", list(personas.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ketik pesan..."):
    if not api_key:
        st.info("Masukkan API Key dulu!")
        st.stop()

    genai.configure(api_key=api_key)
    # KITA PAKAI MODEL LAMA YANG PASTI ADA
    model = genai.GenerativeModel('gemini-pro') 

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # TEKNIK MANUAL: Gabungkan instruksi persona ke dalam pesan
        # Ini mengakali model lama agar tetap punya karakter
        full_prompt = f"Instruksi Sistem: {personas[selected_persona]}\n\nUser bertanya: {prompt}"
        
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        
    st.session_state.messages.append({"role": "assistant", "content": response.text})
