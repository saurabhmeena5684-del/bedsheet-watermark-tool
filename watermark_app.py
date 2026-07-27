# =========================================================
# ================= IMPORTS ===============================
# =========================================================

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from streamlit_cropper import st_cropper
import os
import io
import zipfile
import hashlib

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

if "custom_crop_width" not in st.session_state:
    st.session_state.custom_crop_width = 1080
if "custom_crop_height" not in st.session_state:
    st.session_state.custom_crop_height = 1440

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
    radial-gradient(circle at top left,#1e1b4b 0%,transparent 35%),
    radial-gradient(circle at bottom right,#0f766e 0%,transparent 35%),
    radial-gradient(circle at center,#0a0e1a 0%,transparent 50%),
    linear-gradient(135deg,#020617,#0f172a,#111827);
    color:white;
}

/* ================================================= */
/* ================= MAIN ========================== */
/* ================================================= */

.block-container{
    padding-top:4rem;
    padding-bottom:3rem;
    max-width:100%;
}

/* ================================================= */
/* ================= SIDEBAR ======================= */
/* ================================================= */

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,rgba(7,17,31,0.95) 0%,rgba(4,8,15,0.98) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right:1px solid rgba(255,255,255,0.1);
    box-shadow: 4px 0 30px rgba(0,0,0,0.3);
    min-width:280px !important;
    max-width:280px !important;
}

/* Sidebar sections with glassmorphism */
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider,
section[data-testid="stSidebar"] .stColorPicker,
section[data-testid="stSidebar"] .stCheckbox,
section[data-testid="stSidebar"] .stNumberInput{
    background: rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.06);
    border-radius:16px;
    padding:12px 16px;
    margin-bottom:12px;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stColorPicker label,
section[data-testid="stSidebar"] .stCheckbox label,
section[data-testid="stSidebar"] .stNumberInput label{
    margin-bottom:8px;
}

/* Sidebar selectbox premium style */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]{
    background: rgba(255,255,255,0.05) !important;
    border:1px solid rgba(255,255,255,0.1) !important;
    border-radius:12px !important;
}

section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]:hover{
    border-color:rgba(139,92,246,0.5) !important;
}

/* Sidebar sliders premium style */
section[data-testid="stSidebar"] .stSlider .stSlider > div{
    background: rgba(255,255,255,0.08) !important;
}

section[data-testid="stSidebar"] .stSlider .stSlider > div > div{
    background: linear-gradient(90deg,#8b5cf6,#06b6d4) !important;
}

section[data-testid="stSidebar"] .stSlider .stSlider > div > div > div{
    background: #ffffff !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* Sidebar color picker */
section[data-testid="stSidebar"] .stColorPicker input[type="color"]{
    border-radius:8px;
    border:1px solid rgba(255,255,255,0.15);
    cursor:pointer;
    transition: all 0.3s ease;
}

section[data-testid="stSidebar"] .stColorPicker input[type="color"]:hover{
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(139,92,246,0.3);
}

/* Sidebar dividers */
section[data-testid="stSidebar"] hr{
    border-color: rgba(255,255,255,0.08) !important;
    margin:16px 0;
}

/* ================================================= */
/* ================= TITLE ========================= */
/* ================================================= */

.main-title{
    text-align:center;
    margin:0;
    padding:0;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
}

.main-title h1{
    margin:0;
    padding:0;
    font-size:clamp(28px,4vw,44px) !important;
    font-weight:800 !important;
    background: linear-gradient(90deg,#8b5cf6,#06b6d4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    line-height:1.2;
    word-wrap:break-word;
    overflow:visible;
    text-shadow: 0 0 40px rgba(139,92,246,0.3);
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    margin:0.75rem 0 1.5rem 0;
    font-size:clamp(12px,2vw,14px);
    line-height:1.5;
    font-weight:400;
}

/* ================================================= */
/* ================= SIDEBAR LOGO ================== */
/* ================================================= */

.sidebar-logo{
    display:flex;
    justify-content:center;
    align-items:center;
    margin-top:12px;
    padding:8px;
    background: rgba(255,255,255,0.02);
    border-radius:16px;
    border:1px solid rgba(255,255,255,0.05);
}

.sidebar-title{
    text-align:center;
    font-size:20px;
    font-weight:700;
    margin-top:8px;
    margin-bottom:12px;
    color:#ffffff;
}

/* ================================================= */
/* ================= BUTTONS ======================= */
/* ================================================= */

.stButton button, .stDownloadButton button{
    width:100%;
    border-radius:16px !important;
    height:50px;
    font-weight:600;
    font-size:15px;
    transition: all 0.3s ease;
    color:#ffffff;
}

.stButton button{
    background: linear-gradient(135deg,rgba(139,92,246,0.15),rgba(6,182,212,0.15));
    border:1px solid rgba(139,92,246,0.3) !important;
}

.stButton button:hover{
    box-shadow: 0 8px 25px rgba(139,92,246,0.4);
}

.stDownloadButton button{
    background: linear-gradient(135deg,#8b5cf6,#06b6d4) !important;
    border:none !important;
    box-shadow: 0 4px 20px rgba(139,92,246,0.4);
}

.stDownloadButton button:hover{
    box-shadow: 0 8px 30px rgba(139,92,246,0.5);
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton button{
    background: linear-gradient(135deg,rgba(139,92,246,0.2),rgba(6,182,212,0.2));
    border:1px solid rgba(139,92,246,0.3) !important;
}

section[data-testid="stSidebar"] .stButton button:hover{
    background: linear-gradient(135deg,rgba(139,92,246,0.3),rgba(6,182,212,0.3));
    box-shadow: 0 8px 25px rgba(139,92,246,0.4);
}

/* ================================================= */
/* ================= FILE UPLOADER ================= */
/* ================================================= */

[data-testid="stFileUploader"]{
    background: linear-gradient(135deg,rgba(139,92,246,0.05),rgba(6,182,212,0.05));
    border:2px dashed rgba(139,92,246,0.4);
    border-radius:20px;
    padding:24px;
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"]:hover{
    border-color:rgba(139,92,246,0.7);
    background: linear-gradient(135deg,rgba(139,92,246,0.1),rgba(6,182,212,0.1));
    box-shadow: 0 8px 30px rgba(139,92,246,0.15);
}

[data-testid="stFileUploader"] p{
    color:#cbd5e1;
    font-size:14px;
}

/* ================================================= */
/* ================= IMAGE ========================= */
/* ================================================= */

.stImage img{
    border-radius:20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    transition: box-shadow 0.3s ease;
}

.stImage img:hover{
    box-shadow: 0 12px 40px rgba(139,92,246,0.3);
}

/* ================================================= */
/* ================= WATERMARK CARD ================ */
/* ================================================= */

.preview-card{
    background: linear-gradient(145deg,rgba(255,255,255,0.04),rgba(255,255,255,0.02));
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    padding:12px;
    margin-bottom:12px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.preview-card:hover{
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(139,92,246,0.2);
    border-color:rgba(139,92,246,0.3);
}

.preview-card img{
    border-radius:16px;
}

/* ================================================= */
/* ================= CROP CARD ===================== */
/* ================================================= */

.crop-card{
    background: linear-gradient(145deg,rgba(255,255,255,0.04),rgba(255,255,255,0.02));
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    padding:10px;
    margin-bottom:10px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.crop-card:hover{
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(6,182,212,0.2);
    border-color:rgba(6,182,212,0.3);
}

/* ================================================= */
/* ================= SMALL GAP ===================== */
/* ================================================= */

.element-container{
    margin-bottom:0.5rem !important;
}

[data-testid="column"]{
    padding:0.5rem !important;
}

/* ================================================= */
/* ================= CROPPER ======================= */
/* ================================================= */

iframe{
    border-radius:20px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3) !important;
    border:1px solid rgba(255,255,255,0.1) !important;
}

/* ================================================= */
/* ================= IMAGE HEIGHT ================== */
/* ================================================= */

canvas{
    max-height:240px !important;
    object-fit:contain !important;
    border-radius:16px;
}

/* ================================================= */
/* ================= CHECKBOX ====================== */
/* ================================================= */

.stCheckbox{
    margin-top:4px;
    margin-bottom:4px;
    padding:8px 12px;
    background: rgba(255,255,255,0.02);
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.05);
    transition: all 0.2s ease;
}

.stCheckbox:hover{
    background: rgba(255,255,255,0.04);
    border-color:rgba(139,92,246,0.3);
}

.stCheckbox input[type="checkbox"]{
    accent-color:#8b5cf6;
}

/* ================================================= */
/* ================= FILENAME ====================== */
/* ================================================= */

.filename{
    text-align:center;
    color:#ffffff;
    font-size:11px;
    margin-bottom:4px;
    word-break:break-word;
    font-weight:500;
    text-shadow: 0 1px 4px rgba(0,0,0,0.5);
}

/* ================================================= */
/* ================= SIDEBAR TEXT ================== */
/* ================================================= */

label, .stMarkdown, p{
    font-size:14px !important;
    line-height:1.5;
}

/* Sidebar headers */
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .stHeading{
    color:#ffffff;
    font-weight:600;
    margin-bottom:12px;
}

/* Radio buttons */
.stRadio label, .stRadio div{
    margin-bottom:4px;
}

.stRadio label{
    padding:8px 12px;
    border-radius:10px;
    transition: all 0.2s ease;
}

.stRadio label:hover{
    background: rgba(255,255,255,0.05);
}

/* Success messages */
.stSuccess, .stError, .stWarning, .stInfo{
    border-radius:12px;
    padding:12px 16px;
}

/* ================================================= */
/* ================= SCROLLBAR ===================== */
/* ================================================= */

::-webkit-scrollbar{
    width:8px;
    height:8px;
}

::-webkit-scrollbar-track{
    background: rgba(0,0,0,0.2);
    border-radius:4px;
}

::-webkit-scrollbar-thumb{
    background: linear-gradient(180deg,#8b5cf6,#06b6d4);
    border-radius:4px;
}

::-webkit-scrollbar-thumb:hover{
    background: linear-gradient(180deg,#a78bfa,#22d3ee);
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

    fonts_folder = "Poppins"
    font_files = []

    # =================================================
    # ========= ROBUST FONT LOADING ===================
    # =================================================
    # Check if Poppins folder exists and contains fonts
    if os.path.isdir(fonts_folder):
        font_files = sorted([
            f for f in os.listdir(fonts_folder)
            if f.endswith(".ttf")
        ])

    # =================================================
    # ========= FONT CACHING FOR PERFORMANCE =========
    # =================================================

    @st.cache_data
    def load_font(font_path, font_size):
        """Cache loaded fonts to avoid repeated loading."""
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception as e:
            st.error(f"Font loading error: {str(e)}")
            return ImageFont.load_default()

    def get_default_font():
        """Get default font if Poppins is not available."""
        if font_files:
            return os.path.join(fonts_folder, font_files[0])
        return None

    # =================================================
    # ============= WATERMARK TYPE ====================
    # =================================================

    watermark_source = st.sidebar.radio(
        "📝 Choose Watermark Type",
        [
            "Use Image Filename",
            "Use Custom Text",
            "Use Logo / Image",
            "Use Multiple Watermarks"
        ]
    )

    custom_watermark_text = ""
    uploaded_logo = None

    # Show Custom Text input for Custom Text mode or Multiple Watermarks mode
    if watermark_source in ["Use Custom Text", "Use Multiple Watermarks"]:
        custom_watermark_text = st.sidebar.text_input(
            "Custom Watermark Text",
            placeholder="e.g., Clay Craft"
        )

    # Show Logo uploader for Logo mode or Multiple Watermarks mode
    if watermark_source in ["Use Logo / Image", "Use Multiple Watermarks"]:
        uploaded_logo = st.sidebar.file_uploader(
            "Upload Logo / Watermark Image",
            type=["png", "jpg", "jpeg", "webp"],
            key="logo_uploader"
        )

    # =================================================
    # ========= CUSTOMIZE SELECTOR ====================
    # =================================================
    # ONLY show Customize for Multiple Watermarks mode

    edit_watermark = None
    if watermark_source == "Use Multiple Watermarks":
        edit_watermark = st.sidebar.radio(
            "🎯 Customize",
            [
                "Image Filename",
                "Custom Text",
                "Logo / Image"
            ],
            horizontal=True
        )

    # =================================================
    # ========= SESSION STATE FOR SETTINGS ============
    # =================================================

    if "wm_settings" not in st.session_state:
        st.session_state.wm_settings = {
            "image_name": {
                "font_percent": 8,
                "outline_size": 4,
                "margin_percent": 4,
                "text_color": "#FFFFFF",
                "outline_color": "#000000",
                "visibility": 100,
                "font_style": font_files[0] if font_files else "Poppins-Regular.ttf",
                "position": "Top Right",
                "horizontal_position": 50,
                "vertical_position": 50,
                "auto_font": True,
                "glow": False
            },
            "custom_text": {
                "font_percent": 8,
                "outline_size": 4,
                "margin_percent": 4,
                "text_color": "#FFFFFF",
                "outline_color": "#000000",
                "visibility": 100,
                "font_style": font_files[0] if font_files else "Poppins-Regular.ttf",
                "position": "Bottom Right",
                "horizontal_position": 50,
                "vertical_position": 50,
                "auto_font": False,
                "glow": False
            },
            "logo_image": {
                "size_percent": 20,
                "margin_percent": 4,
                "visibility": 100,
                "position": "Bottom Right",
                "horizontal_position": 50,
                "vertical_position": 50,
                "keep_aspect_ratio": True,
                "glow": False
            }
        }

    # Cache for logo image
    if uploaded_logo and "cached_logo" not in st.session_state:
        try:
            st.session_state.cached_logo = Image.open(uploaded_logo).convert("RGBA")
        except Exception as e:
            st.error(f"Error loading logo: {str(e)}")
    elif "cached_logo" in st.session_state and uploaded_logo is None:
        del st.session_state.cached_logo

    # =================================================
    # ========= DETERMINE CURRENT KEY =================
    # =================================================
    # Determine current_key based on watermark_source for single modes
    # or based on edit_watermark for Multiple Watermarks mode

    if watermark_source == "Use Multiple Watermarks":
        if edit_watermark == "Image Filename":
            current_key = "image_name"
        elif edit_watermark == "Custom Text":
            current_key = "custom_text"
        else:
            current_key = "logo_image"
    elif watermark_source == "Use Image Filename":
        current_key = "image_name"
    elif watermark_source == "Use Custom Text":
        current_key = "custom_text"
    else:
        current_key = "logo_image"

    # Get current settings based on key
    current_settings = st.session_state.wm_settings[current_key]

    # Use a stable key for settings controls
    settings_key = edit_watermark if edit_watermark else current_key.replace("_", " ").title()

    with st.sidebar.expander("⚙️ Watermark Settings", expanded=True):

        # Text Watermark Settings (Image Filename and Custom Text)
        if current_key in ["image_name", "custom_text"]:

            st.sidebar.markdown("**Font**")
            current_settings["font_style"] = st.sidebar.selectbox(
                "Font",
                font_files if font_files else ["Default"],
                index=font_files.index(current_settings["font_style"]) if current_settings["font_style"] in font_files else 0,
                key=f"font_style_{settings_key}"
            )

            st.sidebar.markdown("**Text Size**")
            current_settings["font_percent"] = st.sidebar.slider(
                "Text Size",
                2,
                20,
                current_settings["font_percent"],
                key=f"font_percent_{settings_key}"
            )

            st.sidebar.markdown("**Position**")
            current_settings["position"] = st.sidebar.selectbox(
                "Position",
                ["Top Right", "Top Left", "Center", "Bottom Right"],
                index=["Top Right", "Top Left", "Center", "Bottom Right"].index(current_settings["position"]),
                key=f"position_{settings_key}"
            )

            st.sidebar.markdown("**Horizontal Position**")
            current_settings["horizontal_position"] = st.sidebar.slider(
                "Horizontal Position",
                0,
                100,
                current_settings["horizontal_position"],
                key=f"horizontal_position_{settings_key}"
            )

            st.sidebar.markdown("**Vertical Position**")
            current_settings["vertical_position"] = st.sidebar.slider(
                "Vertical Position",
                0,
                100,
                current_settings["vertical_position"],
                key=f"vertical_position_{settings_key}"
            )

            st.sidebar.markdown("**Distance From Edge**")
            current_settings["margin_percent"] = st.sidebar.slider(
                "Distance From Edge",
                1,
                20,
                current_settings["margin_percent"],
                key=f"margin_percent_{settings_key}"
            )

            st.sidebar.markdown("**Text Color**")
            current_settings["text_color"] = st.sidebar.color_picker(
                "Text Color",
                current_settings["text_color"],
                key=f"text_color_{settings_key}"
            )

            st.sidebar.markdown("**Outline Color**")
            current_settings["outline_color"] = st.sidebar.color_picker(
                "Outline Color",
                current_settings["outline_color"],
                key=f"outline_color_{settings_key}"
            )

            st.sidebar.markdown("**Outline Thickness**")
            current_settings["outline_size"] = st.sidebar.slider(
                "Outline Thickness",
                1,
                15,
                current_settings["outline_size"],
                key=f"outline_size_{settings_key}"
            )

            st.sidebar.markdown("**Visibility**")
            current_settings["visibility"] = st.sidebar.slider(
                "Visibility",
                0,
                100,
                current_settings["visibility"],
                key=f"visibility_{settings_key}"
            )

            if current_key == "image_name":
                st.sidebar.markdown("---")
                st.sidebar.markdown("**Features**")
                current_settings["auto_font"] = st.sidebar.checkbox(
                    "Automatically Fit Long File Names",
                    value=current_settings["auto_font"],
                    key=f"auto_font_{settings_key}"
                )

            st.sidebar.markdown("---")
            current_settings["glow"] = st.sidebar.checkbox(
                "Glow Effect",
                value=current_settings["glow"],
                key=f"glow_{settings_key}"
            )

        # Logo/Image Watermark Settings
        elif current_key == "logo_image":

            st.sidebar.markdown("**Position**")
            current_settings["position"] = st.sidebar.selectbox(
                "Position",
                ["Top Right", "Top Left", "Center", "Bottom Right"],
                index=["Top Right", "Top Left", "Center", "Bottom Right"].index(current_settings["position"]),
                key=f"position_{settings_key}"
            )

            st.sidebar.markdown("**Logo Size**")
            current_settings["size_percent"] = st.sidebar.slider(
                "Logo Size",
                5,
                100,
                current_settings["size_percent"],
                key=f"size_percent_{settings_key}"
            )

            st.sidebar.markdown("**Horizontal Position**")
            current_settings["horizontal_position"] = st.sidebar.slider(
                "Horizontal Position",
                0,
                100,
                current_settings["horizontal_position"],
                key=f"horizontal_position_{settings_key}"
            )

            st.sidebar.markdown("**Vertical Position**")
            current_settings["vertical_position"] = st.sidebar.slider(
                "Vertical Position",
                0,
                100,
                current_settings["vertical_position"],
                key=f"vertical_position_{settings_key}"
            )

            st.sidebar.markdown("**Distance From Edge**")
            current_settings["margin_percent"] = st.sidebar.slider(
                "Distance From Edge",
                1,
                20,
                current_settings["margin_percent"],
                key=f"margin_percent_{settings_key}"
            )

            st.sidebar.markdown("**Visibility**")
            current_settings["visibility"] = st.sidebar.slider(
                "Visibility",
                0,
                100,
                current_settings["visibility"],
                key=f"visibility_{settings_key}"
            )

            st.sidebar.markdown("---")
            current_settings["keep_aspect_ratio"] = st.sidebar.checkbox(
                "Keep Original Aspect Ratio",
                value=current_settings["keep_aspect_ratio"],
                key=f"keep_aspect_ratio_{settings_key}"
            )

            current_settings["glow"] = st.sidebar.checkbox(
                "Glow Effect",
                value=current_settings["glow"],
                key=f"glow_{settings_key}"
            )

    # =================================================
    # ============= PREVIEW SIZE ======================
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

        # Filter out deleted images
        files_to_process = [f for f in uploaded_files if f.name not in st.session_state.selected_images]

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(
            zip_buffer,
            "a",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            st.subheader("🖼 Preview")

            cols = st.columns(columns_count)

            # Cache for logo image
            logo_image = None
            if uploaded_logo and "cached_logo" in st.session_state:
                logo_image = st.session_state.cached_logo

            for index, uploaded_file in enumerate(files_to_process):

                try:
                    image = Image.open(uploaded_file).convert("RGBA")
                except Exception as e:
                    st.error(f"Skipped {uploaded_file.name}:\n{str(e)}")
                    continue

                txt_layer = Image.new("RGBA", image.size, (255,255,255,0))

                filename = os.path.splitext(uploaded_file.name)[0]

                # Apply Image Filename watermark if needed
                if watermark_source in ["Use Image Filename", "Use Multiple Watermarks"]:
                    try:
                        name_settings = st.session_state.wm_settings["image_name"]
                        font_size = int(min(image.size[0], image.size[1]) * (name_settings["font_percent"] / 100))
                        font_path = get_default_font()
                        if font_path and name_settings["font_style"] in font_files:
                            font_path = os.path.join(fonts_folder, name_settings["font_style"])
                        font = load_font(font_path, font_size) if font_path else ImageFont.load_default()

                        # Auto-adjust font for long file names
                        if name_settings["auto_font"]:
                            while True:
                                draw_temp = ImageDraw.Draw(txt_layer)
                                bbox = draw_temp.textbbox((0, 0), filename, font=font, stroke_width=name_settings["outline_size"])
                                tw = bbox[2] - bbox[0]
                                if tw <= image.size[0] * 0.45:
                                    break
                                font_size -= 2
                                if font_size < 20:
                                    break
                                font = load_font(font_path, font_size) if font_path else ImageFont.load_default()

                        draw_temp = ImageDraw.Draw(txt_layer)
                        bbox = draw_temp.textbbox((0, 0), filename, font=font, stroke_width=name_settings["outline_size"])
                        tw = bbox[2] - bbox[0]
                        th = bbox[3] - bbox[1]

                        # Calculate position
                        mx = int(image.size[0] * (name_settings["margin_percent"] / 100))
                        my = int(image.size[1] * (name_settings["margin_percent"] / 100))

                        # Base position from preset
                        if name_settings["position"] == "Top Right":
                            x = image.size[0] - tw - mx
                            y = my
                        elif name_settings["position"] == "Top Left":
                            x = mx
                            y = my
                        elif name_settings["position"] == "Center":
                            x = (image.size[0] - tw) // 2
                            y = (image.size[1] - th) // 2
                        else:  # Bottom Right
                            x = image.size[0] - tw - mx
                            y = image.size[1] - th - my

                        # Apply fine positioning sliders
                        x_range = image.size[0] - tw - (2 * mx)
                        y_range = image.size[1] - th - (2 * my)
                        x = mx + (x_range * name_settings["horizontal_position"] / 100)
                        y = my + (y_range * name_settings["vertical_position"] / 100)

                        x = max(15, min(x, image.size[0] - tw - 15))
                        y = max(15, min(y, image.size[1] - th - 15))

                        # Parse color
                        r = int(name_settings["text_color"][1:3], 16)
                        g = int(name_settings["text_color"][3:5], 16)
                        b = int(name_settings["text_color"][5:7], 16)
                        opacity_val = int(name_settings["visibility"] * 255 / 100)

                        # Draw text with outline and glow
                        draw = ImageDraw.Draw(txt_layer)

                        if name_settings["glow"]:
                            glow_layer = Image.new("RGBA", image.size, (255,255,255,0))
                            glow_draw = ImageDraw.Draw(glow_layer)
                            for blur in range(8):
                                glow_draw.text((x, y), filename, font=font, fill=(255,255,255,35))
                            glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(8))
                            txt_layer = Image.alpha_composite(txt_layer, glow_layer)
                            draw = ImageDraw.Draw(txt_layer)

                        # Draw outline
                        for ox in range(-name_settings["outline_size"], name_settings["outline_size"] + 1):
                            for oy in range(-name_settings["outline_size"], name_settings["outline_size"] + 1):
                                draw.text((x + ox, y + oy), filename, font=font, fill=name_settings["outline_color"])

                        draw.text((x, y), filename, font=font, fill=(r, g, b, opacity_val))
                    except Exception as e:
                        st.error(f"Skipped {uploaded_file.name} (watermark error):\n{str(e)}")
                        continue

                # Apply Custom Text watermark if needed
                if watermark_source in ["Use Custom Text", "Use Multiple Watermarks"] and custom_watermark_text:
                    try:
                        custom_settings = st.session_state.wm_settings["custom_text"]
                        font_size = int(min(image.size[0], image.size[1]) * (custom_settings["font_percent"] / 100))
                        font_path = get_default_font()
                        if font_path and custom_settings["font_style"] in font_files:
                            font_path = os.path.join(fonts_folder, custom_settings["font_style"])
                        font = load_font(font_path, font_size) if font_path else ImageFont.load_default()

                        draw_temp = ImageDraw.Draw(txt_layer)
                        bbox = draw_temp.textbbox((0, 0), custom_watermark_text, font=font, stroke_width=custom_settings["outline_size"])
                        tw = bbox[2] - bbox[0]
                        th = bbox[3] - bbox[1]

                        mx = int(image.size[0] * (custom_settings["margin_percent"] / 100))
                        my = int(image.size[1] * (custom_settings["margin_percent"] / 100))

                        if custom_settings["position"] == "Top Right":
                            x = image.size[0] - tw - mx
                            y = my
                        elif custom_settings["position"] == "Top Left":
                            x = mx
                            y = my
                        elif custom_settings["position"] == "Center":
                            x = (image.size[0] - tw) // 2
                            y = (image.size[1] - th) // 2
                        else:
                            x = image.size[0] - tw - mx
                            y = image.size[1] - th - my

                        x_range = image.size[0] - tw - (2 * mx)
                        y_range = image.size[1] - th - (2 * my)
                        x = mx + (x_range * custom_settings["horizontal_position"] / 100)
                        y = my + (y_range * custom_settings["vertical_position"] / 100)

                        x = max(15, min(x, image.size[0] - tw - 15))
                        y = max(15, min(y, image.size[1] - th - 15))

                        r = int(custom_settings["text_color"][1:3], 16)
                        g = int(custom_settings["text_color"][3:5], 16)
                        b = int(custom_settings["text_color"][5:7], 16)
                        opacity_val = int(custom_settings["visibility"] * 255 / 100)

                        draw = ImageDraw.Draw(txt_layer)

                        if custom_settings["glow"]:
                            glow_layer = Image.new("RGBA", image.size, (255,255,255,0))
                            glow_draw = ImageDraw.Draw(glow_layer)
                            for blur in range(8):
                                glow_draw.text((x, y), custom_watermark_text, font=font, fill=(255,255,255,35))
                            glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(8))
                            txt_layer = Image.alpha_composite(txt_layer, glow_layer)
                            draw = ImageDraw.Draw(txt_layer)

                        for ox in range(-custom_settings["outline_size"], custom_settings["outline_size"] + 1):
                            for oy in range(-custom_settings["outline_size"], custom_settings["outline_size"] + 1):
                                draw.text((x + ox, y + oy), custom_watermark_text, font=font, fill=custom_settings["outline_color"])

                        draw.text((x, y), custom_watermark_text, font=font, fill=(r, g, b, opacity_val))
                    except Exception as e:
                        st.error(f"Skipped {uploaded_file.name} (custom text error):\n{str(e)}")
                        continue

                # Apply Logo watermark if needed
                if watermark_source in ["Use Logo / Image", "Use Multiple Watermarks"] and logo_image:
                    try:
                        logo_settings = st.session_state.wm_settings["logo_image"]

                        logo_w, logo_h = logo_image.size
                        target_size = int(min(image.size[0], image.size[1]) * (logo_settings["size_percent"] / 100))

                        if logo_settings["keep_aspect_ratio"]:
                            scale = target_size / min(logo_w, logo_h)
                            new_w = int(logo_w * scale)
                            new_h = int(logo_h * scale)
                        else:
                            new_w, new_h = target_size, target_size

                        logo_resized = logo_image.resize((new_w, new_h), Image.LANCZOS)

                        mx = int(image.size[0] * (logo_settings["margin_percent"] / 100))
                        my = int(image.size[1] * (logo_settings["margin_percent"] / 100))

                        if logo_settings["position"] == "Top Right":
                            x = image.size[0] - new_w - mx
                            y = my
                        elif logo_settings["position"] == "Top Left":
                            x = mx
                            y = my
                        elif logo_settings["position"] == "Center":
                            x = (image.size[0] - new_w) // 2
                            y = (image.size[1] - new_h) // 2
                        else:
                            x = image.size[0] - new_w - mx
                            y = image.size[1] - new_h - my

                        x_range = image.size[0] - new_w - (2 * mx)
                        y_range = image.size[1] - new_h - (2 * my)
                        x = mx + (x_range * logo_settings["horizontal_position"] / 100)
                        y = my + (y_range * logo_settings["vertical_position"] / 100)

                        x = max(15, min(x, image.size[0] - new_w - 15))
                        y = max(15, min(y, image.size[1] - new_h - 15))

                        if logo_settings["glow"]:
                            glow_layer = Image.new("RGBA", image.size, (255,255,255,0))
                            glow_draw = ImageDraw.Draw(glow_layer)
                            glow_layer.paste(logo_resized, (int(x)-3, int(y)-3), logo_resized)
                            glow_layer.paste(logo_resized, (int(x)+3, int(y)+3), logo_resized)
                            glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(5))
                            txt_layer = Image.alpha_composite(txt_layer, glow_layer)

                        logo_resized_with_alpha = logo_resized.copy()
                        if logo_resized_with_alpha.mode == "RGBA":
                            r, g, b, a = logo_resized_with_alpha.split()
                            a = a.point(lambda p: int(p * logo_settings["visibility"] / 100))
                            logo_resized_with_alpha.putalpha(a)

                        txt_layer.paste(logo_resized_with_alpha, (int(x), int(y)), logo_resized_with_alpha)
                    except Exception as e:
                        st.error(f"Skipped {uploaded_file.name} (logo error):\n{str(e)}")
                        continue

                try:
                    final_image = Image.alpha_composite(image, txt_layer).convert("RGB")

                    img_bytes = io.BytesIO()
                    final_image.save(img_bytes, format="JPEG", quality=100)
                    img_bytes.seek(0)

                    zip_file.writestr(uploaded_file.name, img_bytes.read())

                    with cols[index % columns_count]:
                        st.markdown('<div class="preview-card">', unsafe_allow_html=True)
                        st.image(final_image, caption=uploaded_file.name, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Skipped {uploaded_file.name} (save error):\n{str(e)}")
                    continue

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

    # Initialize session state for crop tool
    if "crop_files" not in st.session_state:
        st.session_state.crop_files = []
    if "crop_checkbox_states" not in st.session_state:
        st.session_state.crop_checkbox_states = {}
    if "crop_cropper_states" not in st.session_state:
        st.session_state.crop_cropper_states = {}
    if "crop_upload_fingerprint" not in st.session_state:
        st.session_state.crop_upload_fingerprint = None

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

    # Use session state for custom dimensions
    if crop_mode == "Custom Size":
        st.session_state.custom_crop_width = st.sidebar.number_input(
            "Width",
            min_value=100,
            value=st.session_state.custom_crop_width
        )
        st.session_state.custom_crop_height = st.sidebar.number_input(
            "Height",
            min_value=100,
            value=st.session_state.custom_crop_height
        )

        if st.sidebar.button("Apply Custom Size"):
            st.rerun()

    st.sidebar.markdown("---")

    preview_size = st.sidebar.radio(
        "Preview Size",
        ["Small", "Medium", "Large"],
        horizontal=True
    )

    if preview_size == "Small":
        columns_count = 6
    elif preview_size == "Medium":
        columns_count = 4
    else:
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

    # Handle Deselect All - clear all selections only
    if deselect_all:
        st.session_state.selected_images.clear()
        st.session_state.crop_checkbox_states = {}
        st.rerun()

    # Handle Reset Changes - reset crop boxes and cropper states only (DO NOT delete files)
    if reset_changes:
        st.session_state.custom_crop_width = 1080
        st.session_state.custom_crop_height = 1440
        st.session_state.crop_cropper_states = {}
        st.rerun()

    # Handle Delete Selected - permanently remove selected images from crop_files
    if delete_selected and st.session_state.crop_files:
        files_to_keep = [f for f in st.session_state.crop_files if f["name"] not in st.session_state.selected_images]
        st.session_state.crop_files = files_to_keep
        # Clear states for deleted files
        for name in list(st.session_state.selected_images):
            st.session_state.crop_checkbox_states.pop(f"select_{name}", None)
            st.session_state.crop_cropper_states.pop(f"crop_{name}", None)
        st.session_state.selected_images.clear()
        st.rerun()

    # Process uploaded files ONLY when new files are actually uploaded (content hash change)
    if uploaded_crop_files:
        # Create content hash fingerprint for each file
        file_hashes = []
        for f in uploaded_crop_files:
            f.seek(0)
            file_bytes = f.read()
            file_hash = hashlib.md5(file_bytes).hexdigest()
            file_hashes.append(f"{f.name}:{file_hash}")
        current_fingerprint = "|".join(file_hashes)
        
        # Only update crop_files if fingerprint changed (new upload)
        if st.session_state.crop_upload_fingerprint != current_fingerprint:
            current_files = []
            for f in uploaded_crop_files:
                f.seek(0)
                current_files.append({
                    "name": f.name,
                    "bytes": f.read()
                })
            st.session_state.crop_files = current_files
            st.session_state.crop_upload_fingerprint = current_fingerprint
            # Clear states when new files uploaded
            st.session_state.crop_checkbox_states = {}
            st.session_state.crop_cropper_states = {}
            st.session_state.selected_images.clear()

    # Use stored files
    files_to_process = st.session_state.crop_files

    if files_to_process:

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:

            cols = st.columns(columns_count)

            for index, file_data in enumerate(files_to_process):
                file_name = file_data["name"]
                file_bytes = file_data["bytes"]

                try:
                    image = Image.open(io.BytesIO(file_bytes))
                except Exception as e:
                    st.error(f"Skipped {file_name}:\n{str(e)}")
                    continue

                if crop_mode == "Original":
                    aspect_ratio = None
                elif crop_mode == "Square 1980×1980":
                    aspect_ratio = (1,1)
                elif crop_mode == "Portrait 2160×2880":
                    aspect_ratio = (3,4)
                elif crop_mode == "Custom Size":
                    aspect_ratio = (st.session_state.custom_crop_width, st.session_state.custom_crop_height)

                with cols[index % columns_count]:

                    st.markdown('<div class="crop-card">', unsafe_allow_html=True)

                    # Use filename-based key for checkbox state
                    checkbox_key = f"select_{file_name}"
                    if checkbox_key not in st.session_state.crop_checkbox_states:
                        st.session_state.crop_checkbox_states[checkbox_key] = False

                    selected = st.checkbox(
                        file_name,
                        key=checkbox_key,
                        value=st.session_state.crop_checkbox_states[checkbox_key]
                    )

                    # Update session state and selected_images
                    st.session_state.crop_checkbox_states[checkbox_key] = selected
                    if selected:
                        st.session_state.selected_images.add(file_name)
                    else:
                        st.session_state.selected_images.discard(file_name)

                    st.markdown(f'<div class="filename">{file_name}</div>', unsafe_allow_html=True)

                    # Use filename-based key for cropper
                    cropper_key = f"crop_{file_name}"

                    cropped_img = st_cropper(
                        image,
                        realtime_update=True,
                        box_color='#ffffff',
                        aspect_ratio=aspect_ratio,
                        return_type='image',
                        key=cropper_key
                    )

                    # Store cropper state
                    st.session_state.crop_cropper_states[cropper_key] = True

                    # Convert RGBA to RGB before saving as JPEG
                    if cropped_img.mode != "RGB":
                        cropped_img = cropped_img.convert("RGB")

                    img_bytes = io.BytesIO()
                    cropped_img.save(img_bytes, format="JPEG", quality=100)
                    img_bytes.seek(0)

                    zip_file.writestr(file_name, img_bytes.read())

                    st.markdown('</div>', unsafe_allow_html=True)

        zip_buffer.seek(0)

        st.download_button(
            label="⬇ Download Cropped Images ZIP",
            data=zip_buffer,
            file_name="cropped_images.zip",
            mime="application/zip"
        )

        st.success("All Images Cropped Successfully ✅")
