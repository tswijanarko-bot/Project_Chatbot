import streamlit as st
import google.generativeai as genai

st.title("📡 RADAR MODEL GOOGLE")

# 1. Input API Key
api_key = st.text_input("Tempel API Key di sini:", type="password")

if st.button("SCAN DATABASE GOOGLE"):
    if not api_key:
        st.error("Kunci kosong!")
    else:
        try:
            # Konfigurasi
            genai.configure(api_key=api_key)
            
            # Minta daftar semua model yang ada
            st.info("Sedang menghubungi server Google...")
            models = genai.list_models()
            
            found_models = []
            st.write("--- HASIL SCAN ---")
            
            # Filter hanya model yang bisa chat (generateContent)
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    st.code(m.name) # Tampilkan nama model
                    found_models.append(m.name)
            
            if not found_models:
                st.error("Tidak ada model chat yang ditemukan untuk Key ini.")
            else:
                st.success(f"Ditemukan {len(found_models)} model aktif!")
                
        except Exception as e:
            st.error(f"GAGAL KONEKSI: {e}")
