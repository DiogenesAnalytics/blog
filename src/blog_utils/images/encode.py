"""Encoding images for use in Jupyter notebooks."""

import base64
import io
from typing import Generator
from typing import Iterable

from PIL import Image


def encode_image_to_base64(img: Image.Image, format: str = "JPEG") -> str:
    """Encode a PIL Image.Image object to a base64 string."""
    with io.BytesIO() as buffer:
        # save image to the buffer
        img.save(buffer, format=format)

        # encode the buffer content to base64
        encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_string


def encode_images(
    images: Iterable[Image.Image], format: str = "JPEG"
) -> Generator[str, None, None]:
    """Encode a sequence of PIL Image.Image objects to base64 strings."""
    for img in images:
        yield encode_image_to_base64(img, format)
