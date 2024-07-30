from io import BytesIO
from PIL import Image
import os
import base64
from concurrent.futures import ThreadPoolExecutor


def convert_bulk(path: str, new_dir: str):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    for image_name in os.listdir(path):
        image_path = os.path.join(path, image_name)
        try:
            with Image.open(image_path) as img:

                conv_image = img.convert('RGB')
                conv_image.thumbnail((400, 400))
                new_image_path = os.path.join(new_dir, os.path.splitext(image_name)[0] + ".png")
                conv_image.save(new_image_path, "PNG")
        except Exception as e:
            print(e)
            continue


def pil_image_to_base64(pil_image):
    byte_io = BytesIO()
    pil_image.save(byte_io, format='PNG')
    byte_image = byte_io.getvalue()
    base64_image = base64.b64encode(byte_image).decode('utf-8')
    return base64_image
