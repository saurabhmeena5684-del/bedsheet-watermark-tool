import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import io
import zipfile

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Bedsheet Watermark Tool",
    page_icon="✨",
    layout="wide"
)

# ---------------- PREMIUM UI ---------------- #

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp{
    background: linear-gradient(135deg,#050816,#0f172a,#111827);
    color:white;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1{
    text-align:center;
    font-size:52px !important;
    font-weight:800 !important;
    background: linear-gradient(90deg,#8b5cf6,#06b6d4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.main-subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:30px;
}

section[data-testid="stSidebar"]{
    background:#0b1120;
    border-right:1px solid rgba(255,255,255,0.08);
}

[data-testid="stFileUploader"]{
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    padding:25px;
    border-radius:20px;
}

.stDownloadButton button{
    width:100%;
    height:60px;
    border:none;
    border-radius:16px;
    background: linear-gradient(90deg,#8b5cf6,#06b6d4);
    color:white;
    font-size:18px;
    font-weight:700;
    transition:0.3s;
}

.stDownloadButton button:hover{
    transform:scale(1.02);
}

img{
    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.title("✨ Bedsheet Watermark Tool")

st.markdown(
    '<div class="main-subtitle">Professional Bulk Watermark Tool For Ecommerce Images</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("⚙️ Watermark Settings")

# RESPONSIVE FONT SIZE %

font_percent = st.sidebar.slider(
    "Font Size %",
    2,
    20,
    8
)

outline_size = st.sidebar.slider(
    "Text Boldness",
    1,
    15,
    4
)

margin_percent = st.sidebar.slider(
    "Margin %",
    1,
    20,
    4
)

text_color = st.sidebar.color_picker(
    "Text Color",
    "#FFFFFF"
)

outline_color = st.sidebar.color_picker(
    "Outline Color",
    "#000000"
)

opacity = st.sidebar.slider(
    "Text Opacity",
    50,
    255,
    255
)

font_style = st.sidebar.selectbox(
    "Font Style",
    [
        "arial.ttf",
        "arialbd.ttf"
    ]
)

position_preset = st.sidebar.selectbox(
    "Watermark Position",
    [
        "Top Right",
        "Top Left",
        "Center",
        "Bottom Right"
    ]
)

# ---------------- EXTRA FEATURES ---------------- #

st.sidebar.markdown("---")

auto_font = st.sidebar.checkbox(
    "Auto Adjust Long Names",
    value=True
)

shadow_glow = st.sidebar.checkbox(
    "Enable Premium Glow",
    value=False
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_files = st.file_uploader(
    "📂 Upload Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# ---------------- PROCESS ---------------- #

if uploaded_files:

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "a",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        st.subheader("🖼 Preview")

        cols = st.columns(3)

        for index, uploaded_file in enumerate(uploaded_files):

            image = Image.open(uploaded_file).convert("RGBA")

            width, height = image.size

            txt_layer = Image.new(
                "RGBA",
                image.size,
                (255,255,255,0)
            )

            draw = ImageDraw.Draw(txt_layer)

            filename = os.path.splitext(
                uploaded_file.name
            )[0]

            # ---------------- RESPONSIVE FONT SIZE ---------------- #

            current_font_size = int(
                min(width, height) * (font_percent / 100)
            )

            try:
                font = ImageFont.truetype(
                    font_style,
                    current_font_size
                )
            except:
                font = ImageFont.load_default()

            # ---------------- AUTO LONG NAME ADJUST ---------------- #

            if auto_font:

                while True:

                    bbox = draw.textbbox(
                        (0,0),
                        filename,
                        font=font
                    )

                    text_width = bbox[2] - bbox[0]

                    if text_width <= width * 0.45:
                        break

                    current_font_size -= 2

                    if current_font_size < 20:
                        break

                    font = ImageFont.truetype(
                        font_style,
                        current_font_size
                    )

            # ---------------- TEXT SIZE ---------------- #

            bbox = draw.textbbox(
                (0,0),
                filename,
                font=font
            )

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # ---------------- RELATIVE MARGIN ---------------- #

            margin_x = int(width * (margin_percent / 100))
            margin_y = int(height * (margin_percent / 100))

            # ---------------- POSITION ---------------- #

            if position_preset == "Top Right":

                x = width - text_width - margin_x
                y = margin_y

            elif position_preset == "Top Left":

                x = margin_x
                y = margin_y

            elif position_preset == "Center":

                x = (width - text_width) // 2
                y = (height - text_height) // 2

            elif position_preset == "Bottom Right":

                x = width - text_width - margin_x
                y = height - text_height - margin_y

            # ---------------- SAFETY FIX ---------------- #

            x = max(15, x)
            y = max(15, y)

            if x + text_width > width - 15:
                x = width - text_width - 15

            if y + text_height > height - 15:
                y = height - text_height - 15

            # ---------------- COLORS ---------------- #

            r = int(text_color[1:3], 16)
            g = int(text_color[3:5], 16)
            b = int(text_color[5:7], 16)

            # ---------------- PREMIUM GLOW ---------------- #

            if shadow_glow:

                glow_layer = Image.new(
                    "RGBA",
                    image.size,
                    (255,255,255,0)
                )

                glow_draw = ImageDraw.Draw(glow_layer)

                for blur in range(8):

                    glow_draw.text(
                        (x, y),
                        filename,
                        font=font,
                        fill=(255,255,255,35)
                    )

                glow_layer = glow_layer.filter(
                    ImageFilter.GaussianBlur(8)
                )

                txt_layer = Image.alpha_composite(
                    txt_layer,
                    glow_layer
                )

                draw = ImageDraw.Draw(txt_layer)

            # ---------------- OUTLINE ---------------- #

            for ox in range(
                -outline_size,
                outline_size + 1
            ):

                for oy in range(
                    -outline_size,
                    outline_size + 1
                ):

                    draw.text(
                        (x + ox, y + oy),
                        filename,
                        font=font,
                        fill=outline_color
                    )

            # ---------------- MAIN TEXT ---------------- #

            draw.text(
                (x, y),
                filename,
                font=font,
                fill=(r, g, b, opacity)
            )

            # ---------------- FINAL IMAGE ---------------- #

            final_image = Image.alpha_composite(
                image,
                txt_layer
            ).convert("RGB")

            # ---------------- SAVE ---------------- #

            img_bytes = io.BytesIO()

            final_image.save(
                img_bytes,
                format="JPEG",
                quality=100
            )

            img_bytes.seek(0)

            zip_file.writestr(
                uploaded_file.name,
                img_bytes.read()
            )

            # ---------------- PREVIEW ---------------- #

            with cols[index % 3]:

                st.image(
                    final_image,
                    caption=uploaded_file.name,
                    use_container_width=True
                )

    # ---------------- DOWNLOAD ---------------- #

    zip_buffer.seek(0)

    st.download_button(
        label="⬇ Download All Images ZIP",
        data=zip_buffer,
        file_name="watermarked_images.zip",
        mime="application/zip"
    )

    st.success("All Images Processed Successfully ✅")