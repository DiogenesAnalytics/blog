"""Encoding images for use in Jupyter notebooks."""

import base64
import os
from typing import List
from typing import Tuple


def encode_images_to_base64(
    image_dir: str,
    supported_formats: Tuple[str, ...] = ("jpg", "jpeg", "png"),
) -> List[str]:
    """Encode all images in the specified directory to base64 strings."""
    # store b64 string
    encoded_images: List[str] = []

    # loop through each file in the directory
    for filename in os.listdir(image_dir):
        # check if the file has the correct extension
        if filename.endswith(supported_formats):
            # get path
            image_path = os.path.join(image_dir, filename)

            # open the image file in binary mode
            with open(image_path, "rb") as image_file:
                # read the file and encode it in base64
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

                # add the encoded string to the list
                encoded_images.append(encoded_string)

    # get list of encoded images
    return encoded_images
