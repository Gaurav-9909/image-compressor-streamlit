import streamlit as st
from PIL import Image
import io
import zipfile

# Page configuration
st.set_page_config(
    page_title="Free Image Compressor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit menu/footer
hide_streamlit_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Header
st.title("⚡ Free Image Compressor")

st.markdown("""
Compress **JPG, PNG, and WEBP images instantly** without losing quality.

🚀 Fast • Secure • Free  
Built by **Gaurav Jangra**
""")

st.divider()

# Sidebar settings
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

# Sidebar branding
st.sidebar.markdown("### 👨‍💻 Developer")
st.sidebar.markdown("**Gaurav Jangra**")
st.sidebar.markdown("🚀 Free Image Compression Tool")

# Upload section
st.subheader("📤 Upload Images")

uploaded_files = st.file_uploader(
    "Drag & Drop or Select Images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

compressed_files = []
zip_buffer = io.BytesIO()

total_original = 0
total_compressed = 0

if uploaded_files:

    progress_container = st.empty()
    progress_bar = progress_container.progress(0, text="Starting compression...")

    for i, file in enumerate(uploaded_files):

        image = Image.open(file)

        original_size = file.size / 1024
        total_original += original_size

        if resize_option:
            image = image.resize((int(width), int(height)))

        img_bytes = io.BytesIO()

        if format_option == "JPEG":
            image = image.convert("RGB")

        image.save(img_bytes, format=format_option, quality=quality)
        img_bytes.seek(0)

        compressed_size = len(img_bytes.getvalue()) / 1024
        total_compressed += compressed_size

        reduction = ((original_size - compressed_size) / original_size) * 100

        st.markdown("---")

        st.markdown(f"### 🖼 {file.name}")

        # Show only compressed image
        st.image(img_bytes, caption="Compressed Image", use_container_width=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"📦 Original Size: **{original_size:.2f} KB**")

        with col2:
            st.write(f"📉 Compressed Size: **{compressed_size:.2f} KB**")

        with col3:
            st.write(f"⚡ Reduction: **{reduction:.2f}%**")

        filename = f"compressed_{file.name}"

        st.download_button(
            label="⬇ Download Image",
            data=img_bytes,
            file_name=filename,
            mime=f"image/{format_option.lower()}"
        )

        compressed_files.append((filename, img_bytes.getvalue()))

        progress = int((i + 1) / len(uploaded_files) * 100)

        progress_bar.progress(
            progress,
            text=f"Compressing image {i+1} of {len(uploaded_files)}"
        )

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

    # Compression summary
    st.markdown("---")

    saved = total_original - total_compressed

    st.success(f"""
📊 Compression Summary

Original Size: {total_original:.2f} KB  
Compressed Size: {total_compressed:.2f} KB  
Space Saved: {saved:.2f} KB
""")

# Features section
st.markdown("---")

st.markdown("### 🚀 Why Use This Tool?")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("⚡ Fast image compression")

with col2:
    st.write("🔒 Secure processing")

with col3:
    st.write("💯 Completely free")

# Footer
st.markdown("---")

st.markdown(
"""
<div style="text-align:center;font-size:14px">
Made with ❤️ by <b>Gaurav Jangra</b><br>
Free Online Image Compressor
</div>
""",
unsafe_allow_html=True
)