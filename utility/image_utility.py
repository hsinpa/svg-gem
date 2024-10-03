from PIL import Image, ImageOps
import math


def resize_canvas(old_image_path: str, new_image_path: str, img_type: str = "JPEG",
                  canvas_width: int = 512, canvas_height: int = 512, revert_pixel: bool = False):
    """
    Resize the canvas of old_image_path.

    Store the new image in new_image_path. Center the image on the new canvas.
    """
    im = Image.open(old_image_path).convert("RGB")
    old_width, old_height = im.size

    mode = im.mode
    new_background = (255, 255, 255)
    if len(mode) == 1:  # L, 1
        new_background = (0)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)


    if old_width > old_height:
        wpercent = (canvas_width / old_width)
        hsize = int((float(old_height) * float(wpercent)))
        im = im.resize((canvas_width, hsize), Image.Resampling.BICUBIC)
    else:
        hpercent = (canvas_height / old_height)
        wsize = int((float(old_width) * float(hpercent)))
        im = im.resize((wsize, canvas_height), Image.Resampling.BICUBIC)

    old_width, old_height = im.size

    # Center the image
    x1 = int(math.floor((canvas_width - old_width) / 2))
    y1 = int(math.floor((canvas_height - old_height) / 2))

    new_image = Image.new("RGB", (canvas_width, canvas_height), new_background)

    if revert_pixel:
        im = ImageOps.invert(im)

    new_image.paste(im, (x1, y1, x1 + old_width, y1 + old_height))

    new_image.save(new_image_path, img_type)