# remove_whitespace_batch_app.py

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
import zipfile

st.title("画像の余白一括削除アプリ（ZIP一括ダウンロード対応）")

def remove_whitespace(pil_image, threshold_value):
    img = np.array(pil_image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        cropped = img[y:y+h, x:x+w]
        return Image.fromarray(cropped)
    else:
        return pil_image

threshold = st.slider("背景の白を除去するしきい値", min_value=200, max_value=255, value=250)

uploaded_files = st.file_uploader(
    "複数の画像をアップロードしてください",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"{len(uploaded_files)} 枚の画像を処理します（しきい値：{threshold}）。")

    # ZIP用のバッファ
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            trimmed_image = remove_whitespace(image, threshold)

            # 表示
            st.image(trimmed_image, caption=f"{uploaded_file.name}（余白削除後）", use_column_width=True)

            # 個別ファイル保存（メモリ内）
            img_bytes = io.BytesIO()
            trimmed_image.save(img_bytes, format="PNG")
            zip_file.writestr(f"trimmed_{uploaded_file.name}", img_bytes.getvalue())

    zip_buffer.seek(0)
    st.download_button(
        label="一括ダウンロード（ZIP形式）",
        data=zip_buffer,
        file_name="trimmed_images.zip",
        mime="application/zip"
    )
