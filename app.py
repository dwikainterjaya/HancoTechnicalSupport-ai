import streamlit as st
from google import genai
import pypdf

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Hanco Inverter Support", page_icon="🤖")

# 2. SISTEM LOGIN (Username & Password)
USERNAME_BENAR = "user"
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
        st.error(f"Gagal membaca file PDF {nama_file}: {e}")
        return None

# 3. Validasi Login
if username_input == USERNAME_BENAR and password_input == PASSWORD_BENAR:
    st.sidebar.success("Login Berhasil!")
    
    st.title("🤖 Hanco Inverter AI Technical Support")
    st.write("Aplikasi cerdas multi-model untuk membaca manual book Inverter Hanco otomatis.")

    # FITUR BARU: PILIHAN MODEL INVERTER
    tipe_inverter = st.selectbox(
        "Pilih Model Inverter Hanco yang ingin Anda tanyakan:",
        ("Hanco Seri S18", "Hanco Seri M3")
    )

    # Menentukan file PDF berdasarkan pilihan user
    if tipe_inverter == "Hanco Seri S18":
        nama_file_pdf = "S18 user manual.pdf"
    else:
        nama_file_pdf = "M3 user manual.pdf"

    # Proses ekstraksi teks dari PDF yang dipilih
    referensi_manual = ekstrak_teks_pdf(nama_file_pdf)

    # Form Pertanyaan
    pertanyaan = st.text_input(f"Ketik pertanyaan Anda tentang {tipe_inverter} di sini:")

    if st.button("Tanya AI Technical Support"):
        if not pertanyaan:
            st.warning("Silakan ketik pertanyaan Anda terlebih dahulu!")
        else:
            if referensi_manual:
                with st.spinner(f"AI sedang menganalisis manual book {tipe_inverter}..."):
                    try:
                        api_key_rahasia = st.secrets["GEMINI_API_KEY"]
                        client = genai.Client(api_key=api_key_rahasia)
                        
                        # Berikan instruksi ketat agar AI fokus pada tipe yang dipilih user
                        prompt_sistem = (
                            f"Anda adalah asisten ahli teknis. Jawablah pertanyaan pengguna secara spesifik "
                            f"hanya berdasarkan informasi resmi dari dokumen manual book {tipe_inverter} berikut:\n\n{referensi_manual}\n\n"
                            f"Pertanyaan Pengguna: {pertanyaan}\n"
                            f"Ingat: Jawab dengan teliti sesuai parameter tipe {tipe_inverter}."
                        )
                        
                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=prompt_sistem
                        )
                        
                        st.subheader(f"Hasil Analisis AI untuk {tipe_inverter}:")
                        st.success("Jawaban ditemukan!")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"Terjadi kesalahan sistem: {e}")
else:
    st.title("🤖 Hanco Inverter AI Technical Support")
    st.info("Silakan masukkan Username dan Password yang benar pada panel di sebelah kiri untuk mengakses AI Support.")
    if username_input or password_input:
        st.sidebar.error("Username atau Password salah!")
