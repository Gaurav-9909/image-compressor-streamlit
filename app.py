import streamlit as st
from PIL import Image
import io
import zipfile

# Page Config
st.set_page_config(
    page_title="Free Image Compressor",
    page_icon="⚡",
    layout="wide"
)

# Hide Streamlit Branding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Header
st.title("⚡ Free Image Compressor")

st.markdown("""
Compress **JPG, PNG, and WEBP images instantly** without losing quality.

**Fast • Secure • Free**  
""")

st.divider()

# Sidebar
st.sidebar.title("⚙ Compression Settings")

quality = st.sidebar.slider(
    "Compression Quality",
    min_value=10,
    max_value=100,
    value=70
)

format_option = st.sidebar.selectbox(
    "Output Format",
    ["JPEG", "PNG", "WEBP"]
)

resize_option = st.sidebar.checkbox("Resize Image")

if resize_option:
    width = st.sidebar.number_input("Width", value=800)
    height = st.sidebar.number_input("Height", value=800)

st.sidebar.markdown("---")

# Sidebar Branding
st.sidebar.markdown("### 👨‍💻 Developer")
st.sidebar.markdown("**Gaurav Jangra**")
st.sidebar.markdown("🚀 Free Image Compression Tool")


# Upload Section
st.subheader("📤 Upload Images")

uploaded_files = st.file_uploader(
    "Drag & Drop or Select Images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

compressed_files = []
zip_buffer = io.BytesIO()

if uploaded_files:

    progress_bar = st.progress(0)

    for i, file in enumerate(uploaded_files):

        image = Image.open(file)

        original_size = file.size / 1024
        original_preview = image.copy()

        if resize_option:
            image = image.resize((int(width), int(height)))

        img_bytes = io.BytesIO()

        if format_option == "JPEG":
            image = image.convert("RGB")

        image.save(img_bytes, format=format_option, quality=quality)
        img_bytes.seek(0)

        compressed_size = len(img_bytes.getvalue()) / 1024
        reduction = ((original_size - compressed_size) / original_size) * 100

        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(original_preview, caption="Original Image", use_column_width=True)

        with col2:
            st.image(img_bytes, caption="Compressed Image", use_column_width=True)

        with col3:
            st.write(f"📦 Original Size: **{original_size:.2f} KB**")
            st.write(f"📉 Compressed Size: **{compressed_size:.2f} KB**")
            st.write(f"⚡ Reduction: **{reduction:.2f}%**")

            filename = f"compressed_{file.name}"

            st.download_button(
                label="⬇ Download Image",
                data=img_bytes,
                file_name=filename,
                mime=f"image/{format_option.lower()}"
            )

        compressed_files.append((filename, img_bytes.getvalue()))

        progress_bar.progress((i + 1) / len(uploaded_files))

    # ZIP download
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for name, data in compressed_files:
            zipf.writestr(name, data)

    zip_buffer.seek(0)

    st.markdown("### 📦 Download All Images")

    st.download_button(
        label="⬇ Download ZIP",
        data=zip_buffer,
        file_name="compressed_images.zip",
        mime="application/zip"
    )

# Footer Branding
st.markdown("---")

st.markdown(
"""
<div style="text-align:center; padding:10px; font-size:14px;">
Made with ❤️ by <b>Gaurav Jangra</b><br>
</div>
""",
unsafe_allow_html=True
)