import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="Pro Image Compressor", page_icon="🖼️", layout="wide")

st.title("🖼️ Pro Image Compressor")
st.write("Upload multiple images and compress them instantly.")

uploaded_files = st.file_uploader(
    "Drag and Drop Images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

st.sidebar.header("Compression Settings")

quality = st.sidebar.slider("Compression Quality", 10, 100, 70)

format_option = st.sidebar.selectbox(
    "Output Format",
    ["JPEG", "PNG", "WEBP"]
)

resize_option = st.sidebar.checkbox("Resize Image")

if resize_option:
    width = st.sidebar.number_input("Width", value=800)
    height = st.sidebar.number_input("Height", value=800)

compressed_files = []
zip_buffer = io.BytesIO()

if uploaded_files:

    for file in uploaded_files:

        image = Image.open(file)

        original_size = file.size / 1024

        if resize_option:
            image = image.resize((int(width), int(height)))

        img_bytes = io.BytesIO()

        if format_option == "JPEG":
            image = image.convert("RGB")

        image.save(img_bytes, format=format_option, quality=quality)

        img_bytes.seek(0)

        compressed_size = len(img_bytes.getvalue()) / 1024

        reduction = ((original_size - compressed_size) / original_size) * 100

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Compressed Preview", width=300)

        with col2:
            st.write(f"Original Size: {original_size:.2f} KB")
            st.write(f"Compressed Size: {compressed_size:.2f} KB")
            st.write(f"Reduction: {reduction:.2f}%")

        filename = f"compressed_{file.name}"

        st.download_button(
            label=f"Download {filename}",
            data=img_bytes,
            file_name=filename,
            mime=f"image/{format_option.lower()}"
        )

        compressed_files.append((filename, img_bytes.getvalue()))

    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for name, data in compressed_files:
            zipf.writestr(name, data)

    zip_buffer.seek(0)

    st.download_button(
        label="⬇ Download All Images (ZIP)",
        data=zip_buffer,
        file_name="compressed_images.zip",
        mime="application/zip"
    )