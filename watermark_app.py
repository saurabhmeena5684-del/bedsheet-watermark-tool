import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import zipfile

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Bedsheet Watermark Tool",
    layout="wide"
)

# ---------------- PREMIUM CSS ----------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#050816,#0b1023,#111827);
    color:white;
}

/* Main Title */

h1{
    text-align:center;
    font-size:52px !important;
    font-weight:800 !important;
    background: linear-gradient(90deg,#a855f7,#06b6d4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:10px;
}

/* Remove Top Space */

.block-container{
    padding-top:2rem;
}

/* Upload Box */

[data-testid="stFileUploader"]{
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

/* Slider */

div[data-baseweb="slider"]{
    padding-top:15px;
    padding-bottom:15px;
}

/* Buttons */

.stButton button{
    width:100%;
    border-radius:16px;
    height:58px;
    border:none;
    font-size:18px;
    font-weight:700;
    background: linear-gradient(90deg,#9333ea,#2563eb);
    color:white;
    transition:0.3s;
}

.stButton button:hover{
    transform:scale(1.03);
    box-shadow:0 0 25px rgba(168,85,247,0.6);
}

/* Download Button */

.stDownloadButton button{
    width:100%;
    border-radius:16px;
    height:58px;
    border:none;
    font-size:18px;
    font-weight:700;
    background: linear-gradient(90deg,#10b981,#06b6d4);
    color:white;
    transition:0.3s;
}

.stDownloadButton button:hover{
    transform:scale(1.03);
    box-shadow:0 0 25px rgba(16,185,129,0.6);
}

/* Image */

img{
    border-radius:20px;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#0f172a;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("👑 Bedsheet Watermark Tool")

st.write("Premium Bulk Watermark Tool For Ecommerce Images")

# ---------------- SIDEBAR ----------------

st.sidebar.header("⚙️ Watermark Settings")

font_size = st.sidebar.slider("Font Size", 20, 200, 80)

text_color = st.sidebar.color_picker("Text Color", "#FFFFFF")

outline_color = st.sidebar.color_picker("Outline Color", "#000000")

outline_size = st.sidebar.slider("Text Boldness", 1, 10, 4)

top_padding = st.sidebar.slider("Top Position", 0, 300, 30)

right_padding = st.sidebar.slider("Right Position", 0, 300, 20)

# ---------------- FONT STYLE ----------------

font_style = st.sidebar.selectbox(
    "Font Style",
    [
        "arial.ttf",
        "arialbd.ttf",
        "calibri.ttf",
        "times.ttf"
    ]
)

# ---------------- FILE UPLOAD ----------------

uploaded_files = st.file_uploader(
    "📂 Upload Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# ---------------- PROCESS ----------------

if uploaded_files:

    output_folder = "output_images"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    processed_files = []

    st.subheader("🖼️ Preview")

    cols = st.columns(3)

    for index, uploaded_file in enumerate(uploaded_files):

        image = Image.open(uploaded_file).convert("RGB")

        draw = ImageDraw.Draw(image)

        filename = os.path.splitext(uploaded_file.name)[0]

        try:
            font = ImageFont.truetype(font_style, font_size)
        except:
            font = ImageFont.load_default()

        text_width = draw.textlength(filename, font=font)

        x = image.width - text_width - right_padding

        y = top_padding

        # Outline

        for ox in range(-outline_size, outline_size + 1):
            for oy in range(-outline_size, outline_size + 1):

                draw.text(
                    (x + ox, y + oy),
                    filename,
                    font=font,
                    fill=outline_color
                )

        # Main Text

        draw.text(
            (x, y),
            filename,
            font=font,
            fill=text_color
        )

        output_path = os.path.join(output_folder, uploaded_file.name)

        image.save(output_path)

        processed_files.append(output_path)

        with cols[index % 3]:
            st.image(image, caption=uploaded_file.name)

    # ---------------- ZIP DOWNLOAD ----------------

    zip_path = "watermarked_images.zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:

        for file in processed_files:
            zipf.write(file)

    st.download_button(
        label="⬇️ Download All Images ZIP",
        data=open(zip_path, "rb"),
        file_name="watermarked_images.zip",
        mime="application/zip"
    )

    st.success("All Images Processed Successfully ✅")