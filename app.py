import base64
import streamlit as st
from fpdf import FPDF
import os, json
from PIL import Image

# HEX renk kodunu RGB formatına dönüştürme fonksiyonu
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

# Function to load data from JSON file
def load_language_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def get_text(lang):
    try:
        file_path = 'data/languages.json'
        data = load_language_data(file_path)
        # Return the specific text based on language and key
        return data[lang]
    
    except Exception as e:
        # Return a default message 
        return f"Error {e} occured in loading {lang} language."

# Dil Seçimi
st.sidebar.title("Dil Seçimi / Language Selection")
lang = st.sidebar.selectbox("Dilinizi Seçin / Select Your Language", ["Türkçe", "English"])

# Seçilen dile göre metinleri al
text = get_text(lang)

# CSS ile hareketli RGB arka plan ve koyu tema
st.markdown(
    """
    <style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    body {
        background: linear-gradient(270deg, #5a85c7, #85c785, #ffc785);
        background-size: 600% 600%;
        animation: gradient 16s ease infinite;
        color: #D3D3D3;  /* Light grey for body text */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main {
        background-color: #1c2833;  /* Darker background for high contrast */
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    }
    /* Heading styles with different colors */
    h1, h2, h3, h4, h5, h6 {
        color: #87CEEB; /* Sky blue for headings */
    }
    /* Ensuring paragraphs are a different color */
     li {
        color: #D3D3D3 !important; /* Light grey for paragraphs */
    }
    p {
        color: #228B22 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# İletişim Sayfası Fonksiyonu
def contact_page():
    st.title(text["contact_title"])
    st.write(text["contact_description"])
    
    # Profil fotoğrafını gösterme
    developer_photo = text["developer_photo"]
    if developer_photo and os.path.exists(developer_photo):
        st.image(developer_photo, width=200)
    else:
        st.write("Developer photo not present")
        
# UTF-8 destekli FPDF sınıfı
class PDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.load_fonts()

    def load_fonts(self):
        """Yazı tiplerini yükler ve PDF'de kullanıma hazır hale getirir."""
        font_path_normal = os.path.join(os.path.dirname(__file__), 'fonts/DejaVuSans.ttf')
        font_path_bold = os.path.join(os.path.dirname(__file__), 'fonts/dejavu-sans-bold.ttf')
        font_path_italic = os.path.join(os.path.dirname(__file__), 'fonts/DejaVuSans-Oblique.ttf')
        
        if os.path.exists(font_path_normal):
            self.add_font('DejaVu', '', font_path_normal, uni=True)
        if os.path.exists(font_path_bold):
            self.add_font('DejaVu', 'B', font_path_bold, uni=True)
        if os.path.exists(font_path_italic):
            self.add_font('DejaVu', 'I', font_path_italic, uni=True)
        self.set_font('DejaVu', '', 12)

    def add_text(self, text, font_name='DejaVu', font_size=12, font_style='', text_color=(0, 0, 0)):
        self.set_font(font_name, style=font_style, size=font_size)
        self.set_text_color(*text_color)
        self.multi_cell(0, 10, text)

    def add_multiple_texts(self, text_list, font_name='DejaVu', font_size=12, font_style='', text_color=(0, 0, 0)):
        if not self.page_no():
            self.add_page()
        for text in text_list:
            self.add_text(text, font_name, font_size, font_style, text_color)
            self.ln()

    def add_image(self, image_path, x=10, y=None, w=100):
        if not self.page_no():
            self.add_page()
        self.image(image_path, x=x, y=y, w=w)

    def add_table(self, data, col_widths):
        if not self.page_no():
            self.add_page()
        for row in data:
            for i, item in enumerate(row):
                self.cell(col_widths[i], 10, str(item), border=1)
            self.ln()

    def save_pdf(self, filename):
        self.output(filename)

# Otomatik Kaydetme ve Taslak Yönetimi
def auto_save_draft(content, draft_name="draft"):
    with open(f"{draft_name}.txt", "w") as f:
        f.write(content)
    st.success(f"Taslak '{draft_name}' olarak kaydedildi.")

# PDF Önizleme fonksiyonu
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Streamlit arayüzü
def main():
    # Menü Yapısı
    menu = [text["project_title"], text["pdf_creator"], text["system_info_title"], text["feedback"], text["contact_title"]]
    choice = st.sidebar.selectbox("Menü Seçimi", menu)

    if choice == text["project_title"]:
        st.title(text["project_title"])
        st.subheader(text["project_goal"])
        st.write(text["project_details"])

    elif choice == text["pdf_creator"]:
        st.title(text["pdf_creator"])
        st.write(text["pdf_creator_details"])

        # Otomatik kaydetme ve çoklu sayfa desteği
        st.text_input("Belge İsmi", key="document_name")
        content = st.text_area("PDF İçeriği", key="pdf_content")
        auto_save_draft(content)

        # Yazı tipi ve boyutu seçimi
        font_name = st.selectbox("Yazı Tipi", ["DejaVu"])
        font_size = st.slider("Yazı Boyutu", 8, 24, 12)
        font_style = st.selectbox("Yazı Stili", ["Normal", "Bold", "Italic"])
        text_color_hex = st.color_picker("Metin Rengi", "#FFFFFF")
        text_color = hex_to_rgb(text_color_hex)

        if font_style == "Bold":
            font_style = 'B'
        elif font_style == "Italic":
            font_style = 'I'
        else:
            font_style = ''

        # Kullanıcıdan birden fazla metin girişi al
        text_entries = []
        text_entry_count = st.number_input("Metin giriş sayısını belirtin:", min_value=1, max_value=10, value=3)

        for i in range(text_entry_count):
            text_input = st.text_input(f"Metin Girişi {i+1}", "")
            text_entries.append(text_input)

        # Görsel yükleme
        image_file = st.file_uploader("PDF'ye eklemek için bir görsel yükleyin", type=["jpg", "jpeg", "png"])
        img_width = st.slider("Görsel Genişliği", 10, 200, 100)
        img_x = st.slider("Görsel X Pozisyonu", 0, 200, 10)

        # Tablo ekleme
        st.write("PDF'ye tablo eklemek için veri girin:")
        col1, col2, col3 = st.columns(3)
        data = [[col1.text_input(f"Satır {i+1}, Sütun 1", ""), 
                col2.text_input(f"Satır {i+1}, Sütun 2", ""), 
                col3.text_input(f"Satır {i+1}, Sütun 3", "")] for i in range(3)]
        table_style = st.selectbox("Tablo Çizgi Stili", ["Border", "No Border"])

        # PDF oluşturma butonu
        if st.button("PDF Oluştur"):
            if any(text_entries):
                pdf_gen = PDFGenerator()

                # Metin ekleme
                pdf_gen.add_multiple_texts(text_entries, font_name, font_size, font_style, text_color)

                # Görseli PDF'ye ekle
                if image_file is not None:
                    img = Image.open(image_file)
                    temp_image_path = "temp_image.png"
                    img.save(temp_image_path)
                    pdf_gen.add_image(temp_image_path, x=img_x, w=img_width)
                    os.remove(temp_image_path)

                # Tabloyu PDF'ye ekle
                if data:
                    col_widths = [40, 40, 40]
                    pdf_gen.add_table(data, col_widths)

                # PDF'yi oluştur ve önizleme
                pdf_filename = "output.pdf"
                pdf_gen.save_pdf(pdf_filename)
                st.success("PDF oluşturuldu! İndirmeden önce aşağıdan önizleyin:")
                show_pdf(pdf_filename)

                # İndirme düğmesi
                with open(pdf_filename, "rb") as file:
                    btn = st.download_button(
                        label="📥 PDF İndir",
                        data=file,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
            else:
                st.warning("Lütfen en az bir metin girişi yapın!")

    elif choice == text["system_info_title"]:
        st.title(text["system_info_title"])
        st.write(text["system_info_details"])

    elif choice == text["feedback"]:
        st.title(text["feedback"])
        st.write(text["feedback_description"])
        for question in text["feedback_questions"]:
            feedback_response = st.radio(question, ["Excellent", "Good", "Average", "Poor"])
            st.write(f"Your feedback for '{question}': {feedback_response}")
            
    elif choice == text["contact_title"]:
        contact_page()  # İletişim sayfasını göster

if __name__ == "__main__":
    main()
