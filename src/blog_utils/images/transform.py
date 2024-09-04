"""Transform images (e.g. resize, crop, etc)."""

import io
import warnings
from typing import Any
from typing import Generator
from typing import Tuple

from PIL import Image

from .io import open_image_file
from .io import open_images_in_directory


def shrink_image_to_size(
    img: Image.Image,
    target_size_kb: int,
    initial_quality: int = 95,
    min_quality: int = 10,
    reduction_factor: float = 0.9,
    quality_step: int = 5,
    resize_step_factor: float = 0.95,
) -> Image.Image:
    """Shrinks the image to approximate target size."""
    # convert the image to RGB mode if it's not already
    if img.mode != "RGB":
        img = img.convert("RGB")

    # initialize img_resized with the original image
    img_resized = img

    # begin size reduction loop
    while initial_quality >= min_quality:
        # resize the image based on the reduction factor
        width, height = img.size
        img_resized = img.resize(
            (int(width * reduction_factor), int(height * reduction_factor)),
            Image.LANCZOS,
        )

        # use a context manager to handle the BytesIO object
        with io.BytesIO() as output_stream:
            # save to memory buffer
            img_resized.save(output_stream, "JPEG", quality=initial_quality)

            # check image size (in kilobytes)
            file_size_kb: float = len(output_stream.getvalue()) / 1024

            # break the loop if the file size is within the desired range
            if file_size_kb <= target_size_kb:
                return img_resized

        # if not, reduce quality and try again
        initial_quality -= quality_step
        reduction_factor *= resize_step_factor

    # issue a warning if the target size could not be met
    warnings.warn(
        "Unable to reduce image below target size without significant quality loss.",
        UserWarning,
        stacklevel=2,
    )

    # return the last attempted image if the loop ends without meeting the target size
    return img_resized


def shrink_image_at_filepath(
    input_path: str, target_size_kb: int, **kwargs: Any
) -> Image.Image:
    """Shrinks the image at the given file path."""
    # open the image from the file path
    img: Image.Image = open_image_file(input_path)

    # shrink the image
    return shrink_image_to_size(img, target_size_kb, **kwargs)


def shrink_images_in_directory(
    directory: str, target_size_kb: int, **kwargs: Any
) -> Generator[Image.Image, None, None]:
    """Yields resized images from a directory."""
    # Use the image_io module to open images from the directory
    for img in open_images_in_directory(directory):
        # Shrink image and yield the resized image
        yield shrink_image_to_size(img, target_size_kb, **kwargs)


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
