from requests import get
from PIL import Image
from io import BytesIO

def show_image(url,title):
    raw = get(url,timeout=3)
    img = Image.open(BytesIO(raw.content))
    return img.show(title=title)