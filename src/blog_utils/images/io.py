"""IO functions for images."""

import os
from pathlib import Path
from typing import Generator
from typing import List
from typing import Tuple

from PIL import Image


def open_image_file(filepath: str) -> Image.Image:
    """Opens an image file and returns a PIL Image object."""
    return Image.open(filepath)


def open_images_in_directory(directory: str) -> Generator[Image.Image, None, None]:
    """Yields PIL Image objects for all images in a directory."""
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            filepath = os.path.join(directory, filename)
            yield open_image_file(filepath)


def save_image_file(img: Image.Image, filepath: str, format: str = "JPEG") -> None:
    """Saves a PIL Image object to a file."""
    img.save(filepath, format=format)


def save_images_to_directory(
    images: List[Image.Image], directory: str, format: str = "JPEG"
) -> None:
    """Saves a list of PIL Image objects to a directory."""
    os.makedirs(directory, exist_ok=True)
    for i, img in enumerate(images):
        filepath = os.path.join(directory, f"image_{i}.{format.lower()}")
        save_image_file(img, filepath, format=format)


def convert_size(size_in_bytes: int, unit: str) -> float:
    """Converts file size from bytes to the specified unit."""
    # define conversion functions
    unit_factors = {
        "bytes": 1,
        "KB": 1024,
        "MB": 1024**2,
    }

    # raise error
    if unit not in unit_factors:
        raise ValueError(f"Invalid unit {unit!r}. Choose from 'bytes', 'KB', or 'MB'.")

    # calculate size for unit
    return size_in_bytes / unit_factors[unit]


def list_file_sizes(
    directory: str, units: str = "KB"
) -> Generator[Tuple[str, float], None, None]:
    """Lists the sizes of all files in the specified directory."""
    # get path obj
    directory_path = Path(directory)

    # yield file sizes
    for file in directory_path.iterdir():
        if file.is_file():
            yield (file.name, convert_size(file.stat().st_size, units))


def print_file_sizes(directory: str, unit: str = "KB") -> None:
    """Prints the sizes of all files directory."""
    # call list_file_sizes and print the results
    for filename, size in list_file_sizes(directory, unit):
        print(f"{filename}: {size:.2f} {unit}")
