from pathlib import Path

from PIL import Image

image_path = Path(__file__).parent / "sample.png"

with Image.open(image_path) as image:

    print("hi")
