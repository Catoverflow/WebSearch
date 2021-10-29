from requests import get
from PIL import Image
from io import BytesIO

def show_image(url,title):
    raw = get(url)
    img = Image.open(BytesIO(raw.content))
    img.show(title=title)