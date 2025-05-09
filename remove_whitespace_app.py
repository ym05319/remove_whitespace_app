# remove_whitespace_batch_app.py

import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.title("画像の余白一括削除アプリ（しきい値調整付き）")

def remove_whitespace(pil_image, threshold_value):
    img = np.array(pil_image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # しきい値の設定を使って白に近い背景を除去
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        cropped = img[y:y+h, x:x+w]
        return Image.fromarray(cropped)
    else:
        return pil_image  # 完全に白の場合などは元画像を返す

# ユーザーが閾値を選べるスライダー（デフォルト：250）
threshold = st.slider("背景の白を除去するしきい値", min_value=200, max_value=255, value=250)

uploaded_files = st.file_uploader(
    "複数の画像をアップロードしてください",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"{len(uploaded_files)} 枚の画像を処理します（しきい値：{threshold}）。")

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        trimmed_image = remove_whitespace(image, threshold)

        st.image(
            trimmed_image,
            caption=f"{uploaded_file.name}（余白削除後）",
            use_column_width=True
        )
