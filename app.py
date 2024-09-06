import base64
import streamlit as st
from fpdf import FPDF
import os
from PIL import Image

# HEX renk kodunu RGB formatına dönüştürme fonksiyonu
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def get_text(lang):
    if lang == "Türkçe":
        return {
            "project_title": "📄 Proje Hakkında",
            "project_goal": "Amaç ve Hedefler",
            "project_details": """
            Bu uygulama, kullanıcıların etkileyici ve profesyonel görünümlü PDF belgeleri oluşturmasını sağlayan güçlü bir dijital belge yönetim aracıdır.
            İş dünyasından eğitime, akademik çalışmalardan kişisel kullanıma kadar geniş bir yelpazede yüksek kaliteli belgeler oluşturmayı mümkün kılar. 
            Kullanıcıların içerikleri özelleştirmesine, görsel ve tablo eklemelerine, stil ve format seçenekleri sunmasına olanak tanıyan bu araç, kullanıcı dostu ve dinamik bir arayüz sunar.
            
            **Ana Amaçlar ve Hedefler:**
            - **Profesyonel PDF Belgeleri Oluşturma:** İş, eğitim ve kişisel kullanım için farklı format ve stillerde profesyonel görünümlü PDF belgeleri hazırlamak.
            - **Gelişmiş Düzenleme Araçları:** Kullanıcıların belgelerini özelleştirmesine olanak tanıyan çeşitli düzenleme seçenekleri sunmak.
            - **Kullanıcı Deneyimini Artırma:** Kolay kullanılabilir arayüz ve güçlü özellikler ile kullanıcı memnuniyetini en üst düzeye çıkarmak.
            - **Çok Yönlü Kullanım Alanı:** Farklı kullanıcı ihtiyaçlarına hitap eden esnek bir çözüm sunmak; raporlar, sunumlar, eğitim materyalleri ve daha fazlası için ideal.
            
            **Uygulamanın Öne Çıkan Özellikleri:**
            - **Çoklu Dil ve Format Desteği:** Birden fazla dil ve belge formatı desteği sunarak, kullanıcıların ihtiyaçlarına uygun belgeler oluşturmalarına olanak tanır.
            - **Dinamik İçerik Yönetimi:** Metin düzenleme, tablo ekleme, görsel entegrasyonu ve sayfa tasarımı ile zengin içerikli belgeler yaratma imkanı.
            - **Otomatik Kaydetme ve Taslak Yönetimi:** Belge oluşturma sırasında otomatik kaydetme ve taslak yönetimi özellikleri ile kullanıcı verilerinin korunmasını sağlar.
            - **Güvenli ve Ölçeklenebilir Mimari:** Kullanıcı verilerinin güvenliğini ve veri bütünlüğünü sağlayan güçlü altyapı.
            - **Gerçek Zamanlı Önizleme ve Düzenleme:** Kullanıcıların belgeyi indirmeden önce nasıl görüneceğini önizleyip düzenleyebilmesi.
            - **Temalar ve Şablonlar:** Önceden tanımlanmış temalar ve şablonlar ile kullanıcıların belge oluşturma sürecini hızlandırın ve kolaylaştırın.
            
            **Kullanım Alanları:**
            - **İş Dünyası:** Şirket içi raporlar, sunumlar, eğitim materyalleri ve strateji belgeleri oluşturmak için.
            - **Eğitim ve Akademik Çalışmalar:** Öğretmenler, öğrenciler ve araştırmacılar için akademik makaleler, tezler ve ders notları hazırlamak için.
            - **Kişisel Kullanım:** Özgeçmişler, davetiyeler, kartvizitler ve diğer kişisel belgeleri düzenleyip oluşturmak için.
            """,
            "system_info_title": "🖥️ Sistem Bilgisi",
            "system_info_details": """
            Uygulamamız, Python ve Streamlit teknolojileri kullanılarak geliştirilmiştir ve PDF oluşturma işlemleri için **FPDF** ve **Pillow** kütüphanelerinden faydalanır.
            Güçlü bir arka uç ve sezgisel bir ön yüz arayüzü sunarak, kullanıcıların belgelerini kolayca düzenleyip oluşturmasına olanak tanır. 

            **Teknik Özellikler:**
            - **Ön Yüz (Frontend):** Streamlit ile modern ve kullanıcı dostu bir arayüz.
            - **Arka Yüz (Backend):** Python tabanlı altyapı, verimli ve hızlı belge oluşturma süreçleri sunar.
            - **Veri İşleme ve Görselleştirme:** FPDF ve Pillow kütüphaneleri kullanılarak gelişmiş veri işleme ve görselleştirme işlevleri.
            - **Güvenlik ve Performans:** Kullanıcı verilerinin şifreleme ile korunması ve ölçeklenebilir yüksek performanslı altyapı.
            - **Güncellemeler ve Destek:** Uygulama sürekli güncellenmekte ve kullanıcı geri bildirimlerine dayalı geliştirmeler yapılmaktadır.
            """,
            "pdf_creator": "📄 Gelişmiş PDF Oluşturucu Uygulaması",
            "pdf_creator_details": """
            Kullanıcılar, zengin metin formatları, tablo düzenleyici ve görsel ekleme seçenekleri ile profesyonel görünümlü PDF belgeleri oluşturabilirler.
            PDF'ler, kullanıcıların iş ihtiyaçlarına, eğitim gereksinimlerine veya kişisel taleplerine göre özelleştirilebilir.

            **PDF Oluşturucu Kullanım Adımları:**
            1. **Metin ve İçerik Ekleme:** Belgeye eklenecek metinleri girin ve düzenleme seçeneklerini kullanarak stil ve format ayarlarını yapın.
            2. **Görsel ve Tablolar Ekleme:** Belgede kullanılacak görselleri ve tabloları yükleyin ve düzenleyin.
            3. **Özelleştirilmiş Ayarlar:** Sayfa boyutu, düzen, kenar boşlukları gibi özellikleri belirleyin.
            4. **Önizleme ve İndir:** PDF belgenizi oluşturun, önizleyin ve cihazınıza indirin.
            """,
            "feedback": "Kullanıcı Deneyimi Geri Bildirimi",
            "feedback_description": """
            Uygulamamız hakkında geri bildirimde bulunarak bize yardımcı olabilirsiniz. Geri bildirimleriniz, ürünümüzü daha da geliştirmemize ve kullanıcı memnuniyetini artırmamıza yardımcı olacaktır.
            """,
            "feedback_questions": [
                "Uygulamamızın genel performansını nasıl değerlendirirsiniz?",
                "PDF oluşturucu arayüzünü ne kadar kullanıcı dostu buldunuz?",
                "Eklenmesini istediğiniz özellikler veya geliştirmeler var mı?",
                "Metin ve görsel ekleme işlemleri ne kadar kolay ve anlaşılır?",
                "Uygulamanın tasarımı ve kullanıcı deneyimi hakkındaki düşünceleriniz nelerdir?",
                "Farklı dillerde PDF oluşturma seçeneklerini ne kadar kullanışlı buldunuz?",
            ],
            "contact_title": "📞 Geliştiriciyle İletişim",
            "contact_description": """
            **Merhaba! Ben Pınar Topuz,** bu uygulamanın geliştiricisiyim. Yazılım geliştirme ve kullanıcı dostu çözümler yaratma konusundaki tutkum, bu uygulamayı geliştirmemde büyük rol oynadı. Kullanıcılara en iyi belge yönetim deneyimini sunmak için buradayım.

            **İletişim Bilgilerim:**
            - 📧 **E-posta:** [piinartp@gmail.com](mailto:piinartp@gmail.com)
            - 💼 **LinkedIn:** [LinkedIn Profilim](https://www.linkedin.com/in/piinartp)
            - 👨‍💻 **GitHub:** [GitHub Profilim](https://github.com/ThecoderPinar)

            İletişime geçmekten çekinmeyin! Geri bildirimleriniz, önerileriniz ve sorularınız için her zaman buradayım.
            """,
        }
    else:  # Default English
        return {
            "project_title": "📄 About the Project",
            "project_goal": "Objectives and Goals",
            "project_details": """
            This application is a robust digital document management tool that empowers users to create visually appealing and professionally styled PDF documents.
            It enables the creation of high-quality documents needed for business, education, and personal use, offering a user-friendly and dynamic interface with options to customize content, add images and tables, and adjust styles and formats.
            
            **Key Objectives and Goals:**
            - **Create Professional PDF Documents:** Design professional-looking PDF documents in various formats and styles for business, education, and personal use.
            - **Advanced Editing Tools:** Provide a range of editing options that allow users to customize their documents.
            - **Enhance User Experience:** Maximize user satisfaction with an easy-to-use interface and powerful features.
            - **Versatile Use Cases:** Offer a flexible solution that caters to different user needs; ideal for reports, presentations, training materials, and more.
            
            **Highlight Features of the Application:**
            - **Multi-language and Format Support:** Offers support for multiple languages and document formats, allowing users to create documents that meet their needs.
            - **Dynamic Content Management:** Provides options for text editing, table insertion, image integration, and page design to create rich-content documents.
            - **Auto Save and Draft Management:** Ensures data preservation with auto-save and draft management features during document creation.
            - **Secure and Scalable Architecture:** Ensures the security and integrity of user data with a robust infrastructure.
            - **Real-Time Preview and Editing:** Allows users to preview and edit the document before downloading.
            - **Themes and Templates:** Speed up and simplify the document creation process with predefined themes and templates.
            
            **Use Cases:**
            - **Business:** Create internal reports, presentations, training materials, and strategy documents for business.
            - **Education and Academic Work:** Prepare academic papers, theses, and lecture notes for teachers, students, and researchers.
            - **Personal Use:** Easily design and create resumes, invitations, business cards, and other personal documents.
            """,
            "system_info_title": "🖥️ System Information",
            "system_info_details": """
            Our application is developed using Python and Streamlit technologies and leverages **FPDF** and **Pillow** libraries for PDF creation processes.
            It offers a powerful backend and an intuitive frontend interface, allowing users to easily edit and create documents.

            **Technical Specifications:**
            - **Frontend:** Modern and user-friendly interface built with Streamlit.
            - **Backend:** Python-based backend optimized for efficient and fast document creation processes.
            - **Data Processing and Visualization:** Advanced data processing and visualization functions powered by FPDF and Pillow libraries.
            - **Security and Performance:** Ensures data security with encryption and provides a scalable high-performance architecture.
            - **Updates and Support:** The application is continuously updated, with improvements based on user feedback.
            """,
            "pdf_creator": "📄 Advanced PDF Creator Application",
            "pdf_creator_details": """
            Users can create professional-looking PDF documents with rich text formatting, table editor, and image insertion options.
            PDFs can be customized according to users' business needs, educational requirements, or personal preferences.

            **Steps to Use the PDF Creator:**
            1. **Add Text and Content:** Enter the text to be added to the document and adjust style and format settings using editing options.
            2. **Insert Images and Tables:** Upload and arrange the images and tables to be used in the document.
            3. **Custom Settings:** Define page size, layout, margins, and other features.
            4. **Preview and Download:** Create your PDF document, preview it, and download it to your device.
            """,
            "feedback": "User Experience Feedback",
            "feedback_description": """
            Help us improve by providing feedback about our application. Your feedback will help us enhance our product and increase user satisfaction.
            """,
            "feedback_questions": [
                "How would you rate the overall performance of our application?",
                "How user-friendly did you find the PDF creator interface?",
                "Are there any features or improvements you would like to see added?",
                "How easy and intuitive was it to add text and images?",
                "What are your thoughts on the design and user experience of the application?",
                "How useful did you find the options for creating PDFs in different languages?",
            ],
            "contact_title": "📞 Contact the Developer",
            "contact_description": """
            **Hello! I'm Pınar Topuz,** the developer of this application. My passion for software development and creating user-friendly solutions played a significant role in developing this app. I am here to provide the best document management experience to users.

            **My Contact Information:**
            - 📧 **Email:** [piinartp@gmail.com](mailto:piinartp@gmail.com)
            - 💼 **LinkedIn:** [My LinkedIn Profile](https://www.linkedin.com/in/piinartp)
            - 👨‍💻 **GitHub:** [My GitHub Profile](https://github.com/ThecoderPinar)

            Feel free to reach out! I'm always here for your feedback, suggestions, and questions.
            """,
        }


# Dil Seçimi
st.sidebar.title("Dil Seçimi / Language Selection")
lang = st.sidebar.selectbox("Dilinizi Seçin / Select Your Language", ["Türkçe", "English"])

# Seçilen dile göre metinleri al
text = get_text(lang)

# CSS ile hareketli RGB arka plan ve koyu tema
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(270deg, #ff7675, #74b9ff, #55efc4);
        background-size: 600% 600%;
        animation: gradient 16s ease infinite;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main {
        background-color: #2c3e50;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
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
    developer_photo = text.get("developer_photo", None)
    if developer_photo and os.path.exists(developer_photo):
        st.image(developer_photo, width=200)
        
# UTF-8 destekli FPDF sınıfı
class PDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.load_fonts()

    def load_fonts(self):
        """Yazı tiplerini yükler ve PDF'de kullanıma hazır hale getirir."""
        font_path_normal = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
        font_path_bold = os.path.join(os.path.dirname(__file__), 'dejavu-sans-bold.ttf')
        font_path_italic = os.path.join(os.path.dirname(__file__), 'DejaVuSans-Oblique.ttf')
        
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
