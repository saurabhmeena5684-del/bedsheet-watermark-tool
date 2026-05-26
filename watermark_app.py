# =========================================================
# ================= IMPORTS ===============================
# =========================================================

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from streamlit_cropper import st_cropper
import os
import io
import zipfile

# =========================================================
# ================= PAGE CONFIG ===========================
# =========================================================

logo = Image.open("logo.png")

st.set_page_config(
    page_title="Watermark Tool",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ================= SESSION ===============================
# =========================================================

if "selected_images" not in st.session_state:
    st.session_state.selected_images = set()

# =========================================================
# ================= CSS ===================================
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ================================================= */
/* ================= BACKGROUND ==================== */
/* ================================================= */

.stApp{
    background:
    radial-gradient(circle at top left,#1e1b4b 0%,transparent 30%),
    radial-gradient(circle at bottom right,#0f766e 0%,transparent 30%),
    linear-gradient(135deg,#020617,#0f172a,#111827);
    color:white;
}

/* ================================================= */
/* ================= MAIN ========================== */
/* ================================================= */

.block-container{
    padding-top:0.3rem;
    max-width:100%;
}

/* ================================================= */
/* ================= SIDEBAR ======================= */
/* ================================================= */

section[data-testid="stSidebar"]{
    background:#07111f;
    border-right:1px solid rgba(255,255,255,0.08);
    min-width:280px !important;
    max-width:280px !important;
}

/* ================================================= */
/* ================= TITLE ========================= */
/* ================================================= */

.main-title{
    text-align:center;
    margin-top:-10px;
}

.main-title h1{
    margin-bottom:0px;
    font-size:44px !important;
    font-weight:800 !important;
    background: linear-gradient(90deg,#8b5cf6,#06b6d4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-top:-5px;
    margin-bottom:15px;
    font-size:14px;
}

/* ================================================= */
/* ================= SIDEBAR LOGO ================== */
/* ================================================= */

.sidebar-logo{
    display:flex;
    justify-content:center;
    align-items:center;
    margin-top:8px;
}

.sidebar-title{
    text-align:center;
    font-size:20px;
    font-weight:700;
    margin-top:-5px;
    margin-bottom:15px;
}

/* ================================================= */
/* ================= BUTTONS ======================= */
/* ================================================= */

.stButton button{
    width:100%;
    border-radius:12px;
    height:42px;
    font-weight:600;
}

.stDownloadButton button{
    width:100%;
    border:none;
    border-radius:14px;
    background: linear-gradient(90deg,#8b5cf6,#06b6d4);
    color:white;
    font-size:15px;
    font-weight:700;
    height:48px;
}

/* ================================================= */
/* ================= FILE UPLOADER ================= */
/* ================================================= */

[data-testid="stFileUploader"]{
    background: rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.06);
    border-radius:14px;
    padding:10px;
}

/* ================================================= */
/* ================= IMAGE ========================= */
/* ================================================= */

.stImage img{
    border-radius:12px;
}

/* ================================================= */
/* ================= WATERMARK CARD ================ */
/* ================================================= */

.preview-card{
    background: rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.05);
    border-radius:14px;
    padding:6px;
    margin-bottom:8px;
}

/* ================================================= */
/* ================= CROP CARD ===================== */
/* ================================================= */

.crop-card{
    background: rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.05);
    border-radius:14px;
    padding:4px;
    margin-bottom:6px;
}

/* ================================================= */
/* ================= SMALL GAP ===================== */
/* ================================================= */

.element-container{
    margin-bottom:0rem !important;
}

[data-testid="column"]{
    padding:0.08rem !important;
}

/* ================================================= */
/* ================= CROPPER ======================= */
/* ================================================= */

iframe{
    border-radius:12px !important;
}

/* ================================================= */
/* ================= IMAGE HEIGHT ================== */
/* ================================================= */

canvas{
    max-height:240px !important;
    object-fit:contain !important;
}

/* ================================================= */
/* ================= CHECKBOX ====================== */
/* ================================================= */

.stCheckbox{
    margin-top:-8px;
    margin-bottom:-8px;
}

/* ================================================= */
/* ================= FILENAME ====================== */
/* ================================================= */

.filename{
    text-align:center;
    color:#ffffff;
    font-size:10px;
    margin-bottom:3px;
    word-break:break-word;
}

/* ================================================= */
/* ================= SIDEBAR TEXT ================== */
/* ================================================= */

label, .stMarkdown, p{
    font-size:14px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# ================= TITLE ================================
# =========================================================

st.markdown("""
<div class="main-title">
    <h1>✨ Watermark Tool</h1>
</div>

<div class="subtitle">
Professional Bulk Watermark & Crop Studio
</div>
""", unsafe_allow_html=True)

# =========================================================
# ================= SIDEBAR ===============================
# =========================================================

st.sidebar.markdown(
    '<div class="sidebar-logo">',
    unsafe_allow_html=True
)

st.sidebar.image(
    logo,
    width=90
)

st.sidebar.markdown(
    '</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-title">Watermark Tool</div>',
    unsafe_allow_html=True
)

# =========================================================
# ================= TOOL SELECTOR =========================
# =========================================================

selected_tool = st.sidebar.selectbox(
    "Select Tool",
    [
        "Watermark Tool",
        "Bulk Crop Tool"
    ]
)

# =========================================================
# ================= WATERMARK TOOL ========================
# =========================================================

if selected_tool == "Watermark Tool":

    st.sidebar.header("⚙️ Watermark Settings")

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

    # =================================================
    # ================= FONT SYSTEM ===================
    # =================================================

    fonts_folder = "Poppins"

    font_files = sorted([
        f for f in os.listdir(fonts_folder)
        if f.endswith(".ttf")
    ])

    font_style = st.sidebar.selectbox(
        "Font Style",
        font_files
    )

    selected_font_path = os.path.join(
        fonts_folder,
        font_style
    )

    # =================================================
    # ================= POSITION ======================
    # =================================================

    position_preset = st.sidebar.selectbox(
        "Watermark Position",
        [
            "Top Right",
            "Top Left",
            "Center",
            "Bottom Right"
        ]
    )

    # =================================================
    # ================= FEATURES ======================
    # =================================================

    st.sidebar.markdown("---")

    auto_font = st.sidebar.checkbox(
        "Auto Adjust Long Names",
        value=True
    )

    shadow_glow = st.sidebar.checkbox(
        "Enable Premium Glow",
        value=False
    )

    # =================================================
    # ================= PREVIEW SIZE ==================
    # =================================================

    st.sidebar.markdown("---")

    preview_size = st.sidebar.radio(
        "Preview Size",
        [
            "Small",
            "Medium",
            "Large"
        ],
        horizontal=True,
        key="watermark_preview"
    )

    if preview_size == "Small":
        columns_count = 6

    elif preview_size == "Medium":
        columns_count = 4

    else:
        columns_count = 2

    # =================================================
    # ================= UPLOAD ========================
    # =================================================

    uploaded_files = st.file_uploader(
        "📂 Upload Images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    # =================================================
    # ================= PROCESS =======================
    # =================================================

    if uploaded_files:

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(
            zip_buffer,
            "a",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            st.subheader("🖼 Preview")

            cols = st.columns(columns_count)

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

                current_font_size = int(
                    min(width, height) * (font_percent / 100)
                )

                try:

                    font = ImageFont.truetype(
                        selected_font_path,
                        current_font_size
                    )

                except:

                    font = ImageFont.load_default()

                # =========================================
                # ================= AUTO FONT =============
                # =========================================

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
                            selected_font_path,
                            current_font_size
                        )

                bbox = draw.textbbox(
                    (0,0),
                    filename,
                    font=font
                )

                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                margin_x = int(width * (margin_percent / 100))
                margin_y = int(height * (margin_percent / 100))

                # =========================================
                # ================= POSITION ==============
                # =========================================

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

                x = max(15, x)
                y = max(15, y)

                r = int(text_color[1:3], 16)
                g = int(text_color[3:5], 16)
                b = int(text_color[5:7], 16)

                # =========================================
                # ================= GLOW ==================
                # =========================================

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

                # =========================================
                # ================= OUTLINE ===============
                # =========================================

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

                # =========================================
                # ================= MAIN TEXT =============
                # =========================================

                draw.text(
                    (x, y),
                    filename,
                    font=font,
                    fill=(r, g, b, opacity)
                )

                final_image = Image.alpha_composite(
                    image,
                    txt_layer
                ).convert("RGB")

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

                with cols[index % columns_count]:

                    st.markdown(
                        '<div class="preview-card">',
                        unsafe_allow_html=True
                    )

                    st.image(
                        final_image,
                        caption=uploaded_file.name,
                        use_container_width=True
                    )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

        zip_buffer.seek(0)

        st.download_button(
            label="⬇ Download All Images ZIP",
            data=zip_buffer,
            file_name="watermarked_images.zip",
            mime="application/zip"
        )

        st.success("All Images Processed Successfully ✅")

# =========================================================
# ================= BULK CROP TOOL ========================
# =========================================================

elif selected_tool == "Bulk Crop Tool":

    st.sidebar.header("✂️ Crop Settings")

    crop_mode = st.sidebar.selectbox(
        "Crop Mode",
        [
            "Original",
            "Square 1980×1980",
            "Portrait 2160×2880",
            "Custom Size"
        ]
    )

    custom_width = 1080
    custom_height = 1440

    if crop_mode == "Custom Size":

        col1, col2 = st.sidebar.columns(2)

        with col1:

            custom_width = st.number_input(
                "Width",
                min_value=100,
                value=1080
            )

        with col2:

            custom_height = st.number_input(
                "Height",
                min_value=100,
                value=1440
            )

        st.sidebar.button("Apply Custom Size")

    st.sidebar.markdown("---")

    preview_size = st.sidebar.radio(
        "Preview Size",
        [
            "Small",
            "Medium",
            "Large"
        ],
        horizontal=True
    )

    if preview_size == "Small":
        columns_count = 6

    elif preview_size == "Medium":
        columns_count = 4

    elif preview_size == "Large":
        columns_count = 2

    st.sidebar.markdown("---")

    deselect_all = st.sidebar.button("Deselect All")

    delete_selected = st.sidebar.button("Delete Selected")

    reset_changes = st.sidebar.button("Reset Changes")

    uploaded_crop_files = st.file_uploader(
        "📂 Upload Images For Cropping",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="crop_upload"
    )

    if deselect_all:
        st.session_state.selected_images.clear()

    if reset_changes:
        crop_mode = "Original"

    if uploaded_crop_files:

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(
            zip_buffer,
            "a",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            cols = st.columns(columns_count)

            for index, uploaded_file in enumerate(uploaded_crop_files):

                image = Image.open(uploaded_file)

                if crop_mode == "Original":

                    aspect_ratio = None

                elif crop_mode == "Square 1980×1980":

                    aspect_ratio = (1,1)

                elif crop_mode == "Portrait 2160×2880":

                    aspect_ratio = (3,4)

                elif crop_mode == "Custom Size":

                    aspect_ratio = (
                        custom_width,
                        custom_height
                    )

                with cols[index % columns_count]:

                    st.markdown(
                        '<div class="crop-card">',
                        unsafe_allow_html=True
                    )

                    selected = st.checkbox(
                        uploaded_file.name,
                        key=f"select_{index}"
                    )

                    if selected:
                        st.session_state.selected_images.add(
                            uploaded_file.name
                        )

                    else:
                        st.session_state.selected_images.discard(
                            uploaded_file.name
                        )

                    st.markdown(
                        f'<div class="filename">{uploaded_file.name}</div>',
                        unsafe_allow_html=True
                    )

                    cropped_img = st_cropper(
                        image,
                        realtime_update=True,
                        box_color='#ffffff',
                        aspect_ratio=aspect_ratio,
                        return_type='image',
                        key=f"crop_{index}"
                    )

                    img_bytes = io.BytesIO()

                    cropped_img.save(
                        img_bytes,
                        format="JPEG",
                        quality=100
                    )

                    img_bytes.seek(0)

                    zip_file.writestr(
                        uploaded_file.name,
                        img_bytes.read()
                    )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

        zip_buffer.seek(0)

        st.download_button(
            label="⬇ Download Cropped Images ZIP",
            data=zip_buffer,
            file_name="cropped_images.zip",
            mime="application/zip"
        )

        st.success("All Images Cropped Successfully ✅")