import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image

def load_image(src_url):
    try:
        if src_url.startswith("data:image"):
            return None  # handle base64 separately if needed
        resp = requests.get(src_url, timeout=5)
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception:
        return None

def compute_visual_features(image, x, y, width, height, vw, vh):
    f = {}
    f['F1_vertical_pos'] = y / vh if vh else 0
    f['F2_horizontal_pos'] = x / vw if vw else 0
    f['F3_vertical_region'] = 0 if y < vh / 2 else 1

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f['F4_std_dev'] = float(np.std(gray))

    ratio_hw = height / width if width else 0
    f['F6_dim_ratio'] = abs(1.0 - ratio_hw)

    b, g, r = cv2.split(image.astype("float"))
    rg = np.absolute(r - g)
    yb = np.absolute(0.5 * (r + g) - b)
    f['F7_colourfulness'] = float(np.sqrt(np.std(rg) ** 2 + np.std(yb) ** 2))

    area = width * height
    min_area = 15 * 15
    f['F8_size_score'] = abs((area / min_area) - 1.0)

    f['F5_padding'] = compute_padding(gray)
    return f

def compute_padding(gray_img):
    # Simplified: % of near-zero-variance edge rows/cols
    h, w = gray_img.shape
    if w == 0 or h == 0:
        return 0
    col_std = np.std(gray_img, axis=0)
    zero_cols = np.sum(col_std < 2)
    return zero_cols / w