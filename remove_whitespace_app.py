import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def trim_whitespace_opencv(image, threshold=240):
    # PIL → OpenCV（BGR）
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 白背景をマスク（白っぽいところを除去対象に）
    _, thresh_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # 輪郭抽出（白以外の領域）
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        x, y, w, h = cv2.boundingRect(np.vstack(contours))
        cropped = image[y:y+h, x:x+w]
    else:
        cropped = image  # 内容なしならそのまま

    # OpenCV（BGR）→ PIL（RGB）
    cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cropped_rgb)

st.set_page_config(page_title="画像余白削除ツール", layout="centered")
st.title("🖼️ 画像の余白を自動で削除")
st.write("白い余白を自動検出してトリミングします。")

uploaded_file = st.file_uploader("画像ファイルをアップロード（JPG, PNG）", type=["jpg", "jpeg", "png"])
threshold = st.slider("白とみなす明るさの基準値", 200, 255, 240)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📥 アップロード画像", use_column_width=True)

    trimmed = trim_whitespace_opencv(image, threshold=threshold)
    st.image(trimmed, caption="✂️ 余白削除後", use_column_width=True)

    buf = io.BytesIO()
    trimmed.save(buf, format="PNG")
    st.download_button("⬇️ トリミング後の画像をダウンロード", data=buf.getvalue(),
                       file_name="trimmed.png", mime="image/png")
