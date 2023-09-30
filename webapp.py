import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def resize_image(image, scale_percent):
    width = int(image.width * scale_percent / 100)
    height = int(image.height * scale_percent / 100)
    new_dim = (width, height)
    resized = image.resize(new_dim, Image.LANCZOS)  # Use Image.LANCZOS
    return resized

def compress_image(image, quality):
    buffer = io.BytesIO()
    # Convert image to RGB if it is RGBA
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.save(buffer, format='JPEG', quality=quality)
    compressed_image = Image.open(buffer)
    return compressed_image

st.title('画像のリサイズと圧縮')

uploaded_file = st.file_uploader('画像をアップロードしてください。', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption='アップロードされた画像。', use_column_width=True)

    scale_percent = st.slider('縮小比率 (%)', min_value=1, max_value=100, value=50)
    quality = st.slider('JPEG品質', min_value=1, max_value=100, value=85)

    if st.button('画像を処理'):
        resized_image = resize_image(image, scale_percent)
        compressed_image = compress_image(resized_image, quality)

        st.image(compressed_image, caption='処理後の画像。', use_column_width=True)

        img_stream = io.BytesIO()
        compressed_image.save(img_stream, format='JPEG', quality=quality)
        img_stream.seek(0)
        st.download_button('処理後の画像をダウンロード', data=img_stream, file_name='output.jpg', mime='image/jpeg')
