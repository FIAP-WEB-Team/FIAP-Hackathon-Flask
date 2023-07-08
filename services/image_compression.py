import io
from typing import List
from base64 import encodebytes

from PIL import Image


IMAGE_LIST_SIZE_LIMIT = 1024 * 1000 # Limit size in bytes
MIN_QUALITTY = 1
MAX_QUALITTY = 85


def _save_to_bytes(image: Image, quality: int):
    compressed_image = io.BytesIO()
    image.save(compressed_image, format='JPEG', quality=quality)
    return compressed_image


def _compress_image(image: Image, goal_weight: int):
    l_quality = MIN_QUALITTY
    r_quality = MAX_QUALITTY
    while l_quality <= r_quality:
        mid_quality = int((l_quality + r_quality) / 2)
        compressed_image = _save_to_bytes(image, mid_quality)
        weight = compressed_image.tell()
        if weight > goal_weight:
            r_quality = mid_quality - 1
        else:
            l_quality = mid_quality + 1

    compressed_image = _save_to_bytes(image, r_quality)

    return compressed_image


def compress_images(uploaded_files: list) -> List[bytes]:
    weights = []
    images = [Image.open(file) for file in uploaded_files]
    compressed_images = [_save_to_bytes(image, MAX_QUALITTY) for image in images]
    for compressed_image in compressed_images:
        weights.append(compressed_image.tell())
    sum_weights = sum(weights)

    if sum_weights > IMAGE_LIST_SIZE_LIMIT:
        dt_weight = sum_weights - IMAGE_LIST_SIZE_LIMIT
        weights = [int(weight * (1 - dt_weight / sum_weights)) for weight in weights]

        compressed_images = [_compress_image(image, weight) for image, weight in zip(images, weights)]
    return [encodebytes(compressed_image.getvalue()).decode('ascii') for compressed_image in compressed_images]
