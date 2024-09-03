"""Transform images (e.g. resize, crop, etc)."""

import io
import os
from typing import Tuple

from PIL import Image


def shrink_image_to_size(
    input_path: str,
    output_path: str,
    target_size_kb: int,
    step: int = 5,
    min_quality: int = 10,
) -> None:
    """Shrinks the image to approximately the target size by adjusting its quality."""
    # open image using PIL
    img: Image.Image = Image.open(input_path)

    # convert the image to RGB mode if it's not already
    if img.mode != "RGB":
        img = img.convert("RGB")

    # start with a high quality setting
    quality: int = 95

    # begin size reduction
    while quality >= min_quality:
        # use a BytesIO object to save the image in memory
        with io.BytesIO() as output_stream:
            # save to memory buffer
            img.save(output_stream, "JPEG", quality=quality)

            # get image size
            file_size_kb: float = len(output_stream.getvalue()) / 1024

            # break the loop if the file size is within the desired range
            if file_size_kb <= target_size_kb:
                # save the final image to disk
                with open(output_path, "wb") as final_output_file:
                    final_output_file.write(output_stream.getvalue())
                return  # exit function once the desired size is achieved

        # reduce the quality for the next iteration
        quality -= step

    # if the loop exits without achieving the desired size
    print(
        "Warning: Unable to reduce image below target size "
        "without significant quality loss."
    )


def shrink_images_in_directory(
    directory: str, target_size_kb: int, output_dir: str = "resized_images"
) -> None:
    """Shrinks all images in a directory to the target size by adjusting the quality."""
    # ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # loop over files in dir
    for filename in os.listdir(directory):
        # make sure file is an image
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            # create paths for input/output file
            input_path: str = os.path.join(directory, filename)
            output_path: str = os.path.join(output_dir, filename)

            # now shrink
            shrink_image_to_size(input_path, output_path, target_size_kb)


def crop_to_target(image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
    """Crop the image to fit the target size from the top down."""
    # get current images width/height
    width, height = image.size

    # get corresponding target width/height
    target_width, target_height = target_size

    # resize image with aspect ratio preservation
    if width / height > target_width / target_height:
        new_height = target_height
        new_width = int((width / height) * new_height)
    else:
        new_width = target_width
        new_height = int((height / width) * new_width)

    # now apply resize
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # ensure image is in RGB format for further processing
    if image.mode != "RGB":
        image = image.convert("RGB")

    # calculate cropping box from the top
    left = (new_width - target_width) / 2
    top = 0
    right = (new_width + target_width) / 2
    bottom = target_height

    # ensure cropping box is within image bounds
    if right > new_width:
        right = new_width
        left = right - target_width
    if bottom > new_height:
        bottom = new_height
        top = bottom - target_height

    # convert cropping box coordinates to integers
    left = int(left)
    top = int(top)
    right = int(right)
    bottom = int(bottom)

    # crop and final resize
    image = image.crop((left, top, right, bottom))
    image = image.resize(target_size, Image.Resampling.LANCZOS)

    # voila
    return image
