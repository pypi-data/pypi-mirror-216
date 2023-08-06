from PIL import Image
from fabisschomagut import to_rgb_tuple
from touchtouch import touch
from ignoreexceptions import ignore_Exception
from typing import Any


def resize_with_background(
    image, target_size: int = 512, background=None, background_ratio: int = 1
) -> Image:
    """
    Resize an image to the specified target size with a background.

    Args:
        image (Image, np.array or str (file path)): The input image.
        target_size (int, optional): The target size for the resized image. Defaults to 512.
        background (None, Image, np.array, str (file path/hex color/color name), RGB tuple, optional): The background. Defaults to None (image is also used as background).
        background_ratio (int): Zoom on background pic

    Returns:
        Image: The resized image with the background.
    """
    image = image2rgb(image)
    width, height = fit_pic_to_size(target_size, *image.size)
    resized_image = image.resize((width, height))
    try:
        if not background:
            background = image.copy()
    except ValueError:
        pass
    background_image = create_new_image_with_color(target_size, background)
    if not background_image:
        background_image = resize_image_at_least_size(background, target_size)
        background_image = crop_image(
            background_image, (target_size, target_size), background_ratio
        )
    x = (target_size - width) // 2
    y = (target_size - height) // 2
    background_image.paste(resized_image, (x, y))
    return background_image


def pic2ico(src: Any, dst=None) -> str:
    """
    Convert an image to an ICO file format.

    Args:
        src (Image, np.array or str (file path)): The source image file path.
        dst (str, optional): The destination ICO file path. Defaults to None.

    Returns:
        str: The path to the converted ICO file.
    """
    if not dst and isinstance(src, str):
        dst = src.split(".")
        dst = ".".join(dst[:-1]) + ".ico"
    if not dst:
        raise ValueError("No output defined!")
    touch(dst)
    image2rgb(src).convert("RGB").resize((512, 512)).save(dst)
    return dst


def fit_pic_to_size(target_size: int, width: int, height: int) -> tuple:
    """
    Calculate the new dimensions to fit an image to the specified target size.

    Args:
        target_size (int): The target size.
        width (int): The current width of the image.
        height (int): The current height of the image.

    Returns:
        tuple: The new width and height.
    """
    aspect_ratio = width / height
    if aspect_ratio > 1:
        new_width = target_size
        new_height = int(target_size / aspect_ratio)
    else:
        new_height = target_size
        new_width = int(target_size * aspect_ratio)
    return new_width, new_height


def image2rgb(image) -> Image:
    """
    Convert an image to RGB format.

    Args:
        image (Image, np.array or str (file path)): The input image. It can be a file path or a PIL Image object.

    Returns:
        Image: The image in RGB format.
    """
    if isinstance(image, str):
        image = Image.open(image)
    if "numpy" in str(type(image)).lower():
        image = image[..., ::-1]
        image = Image.fromarray(image)
    return image.convert("RGB")


@ignore_Exception(v=None, print_exceptions=False)
def create_new_image_with_color(target_size, background_color) -> Image:
    """
    Create a new image with a specified background color.

    Args:
        target_size (int): The size of the new image.
        background_color (str or tuple): The background color.

    Returns:
        Image: The new image with the specified background color.
    """
    background_color = to_rgb_tuple(color=background_color, invert=False)
    return Image.new("RGB", (target_size, target_size), background_color)


def crop_image(image, crop_size: tuple | list, background_ratio: int = 1) -> Image:
    """
    Crop an image to the specified size.

    Args:
        image (Image, np.array or str (file path)): The input image.
        crop_size (tuple or list): The size of the cropped image.
        background_ratio (int): Zoom on background pic

    Returns:
        Image: The cropped image.
    """
    image = image2rgb(image)
    imagex = image.resize(
        (image.size[0] * background_ratio, image.size[1] * background_ratio)
    )
    width, height = imagex.size
    x1 = (width - crop_size[0]) // 2
    y1 = (height - crop_size[1]) // 2
    x2 = x1 + crop_size[0]
    y2 = y1 + crop_size[1]
    cropped_image = imagex.crop((x1, y1, x2, y2))
    return cropped_image


def resize_image_at_least_size(image, target_size: int) -> Image:
    """
    Resize an image to at least the specified target size while maintaining the aspect ratio.

    Args:
        image (Image, np.array or str (file path)): The input image.
        target_size (int): The minimum size for the resized image.

    Returns:
        Image: The resized image.
    """
    image = image2rgb(image)
    width, height = image.size
    aspect_ratio = width / height
    if width >= height:
        new_width = max(target_size, width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max(target_size, height)
        new_width = int(new_height * aspect_ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image
