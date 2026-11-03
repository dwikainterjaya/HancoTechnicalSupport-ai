import streamlit as st
from google import genai
import pypdf

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Hanco Inverter Support", page_icon="🤖")

# 2. SISTEM LOGIN (Username & Password)
# Anda bisa mengganti 'admin' dan 'hanco123' sesuai keinginan Anda
USERNAME_BENAR = "admin"
PASSWORD_BENAR = "hanco123"

st.sidebar.header("🔑 Login Sistem")
username_input = st.sidebar.text_input("Username:")
password_input = st.sidebar.text_input("Password:", type="password")

# Fungsi Ekstraksi PDF
@st.cache_resource
def ekstrak_teks_pdf(nama_file):
    try:
        reader = pypdf.PdfReader(nama_file)
        teks_lengkap = ""
        for page in reader.pages:
            teks_lengkap += page.extract_text() + "\n"
        return teks_lengkap
    except Exception as e:
        st.error(f"Gagal membaca file PDF: {e}")
        return None

# Membaca file PDF lokal
referensi_manual = ekstrak_teks_pdf("S18 user manual.pdf")

# 3. Validasi Login
if username_input == USERNAME_BENAR and password_input == PASSWORD_BENAR:
    st.sidebar.success("Login Berhasil!")
    
    # Tampilan Utama Aplikasi setelah login sukses
    st.title("🤖 Hanco Inverter AI Technical Support")
    st.write("Aplikasi cerdas untuk membaca manual book Inverter Hanco Seri S18 secara otomatis.")

    # Form Pertanyaan
    pertanyaan = st.text_input("Ketik pertanyaan Anda di sini (Contoh: Apa arti error E-01?):")

    if st.button("Tanya AI Technical Support"):
        if not pertanyaan:
            st.warning("Silakan ketik pertanyaan Anda terlebih dahulu!")
        else:
            if referensi_manual:
                with st.spinner("AI sedang menganalisis manual book..."):
                    try:
                        # Mengambil API Key secara otomatis dari Streamlit Secrets yang sudah disimpan di Langkah 1
                        api_key_rahasia = st.secrets["GEMINI_API_KEY"]
                        client = genai.Client(api_key=api_key_rahasia)
                        
                        prompt_sistem = (
                            f"Anda adalah asisten ahli teknis. Jawablah pertanyaan pengguna hanya berdasarkan "
                            f"informasi resmi dari dokumen manual book inverter Hanco berikut:\n\n{referensi_manual}\n\n"
                            f"Pertanyaan Pengguna: {pertanyaan}"
                        )
                        
                           response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt_sistem
                            )
                      
                        st.subheader("Hasil Analisis AI:")
                        st.success("Jawaban ditemukan!")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"Terjadi kesalahan sistem: {e}")
else:
    # Tampilan jika belum login atau salah password
    st.title("🤖 Hanco Inverter AI Technical Support")
    st.info("Silakan masukkan Username dan Password yang benar pada panel di sebelah kiri untuk mengakses AI Support.")
    if username_input or password_input:
        st.sidebar.error("Username atau Password salah!")
