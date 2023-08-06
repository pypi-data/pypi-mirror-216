import io
import logging
import zipfile
import os

from PIL import Image, ImageDraw
from js import Uint8Array, File, document, window

from .spec import icon_spec

log = logging.getLogger(__name__)
usage_log = logging.getLogger("mki_usage")


class Processor:
    def __init__(self, png_img):
        self.png_img = png_img
        self.path_stream_tuples = []

    @property
    def method_map(self):
        return {
            "should_crop_to_rounded": self.crop_to_rounded,
            "should_remove_alpha": self.remove_alpha,
            "crop_height": self.crop_height,
            "size": self.resize,
        }

    def remove_alpha(self, img, spec):
        """
        - Convert this to RGBA if possible
        - Black background canvas (r,g,b,a)
        - Paste the image onto the canvas, using it's alpha channel as mask
        """
        img.convert("RGBA")
        canvas = Image.new("RGBA", img.size, (0, 0, 0, 255))
        canvas.paste(img, mask=img)
        canvas.thumbnail([spec["size"], spec["size"]], Image.ANTIALIAS)
        img = canvas.convert("RGB")
        return img

    def crop_height(self, img, spec):
        """
        - Crop icon height for rectangular icon
        """
        crop_height_spec = spec["crop_height"]
        width, height = img.size
        top = (height - crop_height_spec) // 2
        bottom = (height + crop_height_spec) // 2
        img = img.crop((0, top, width, bottom))
        return img

    def crop_to_rounded(self, img, spec):
        """
        - Crop to rounded icon
        """
        circle = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0) + img.size, fill=255)
        alpha = Image.new("L", img.size, 255)
        alpha.paste(circle)
        img.putalpha(alpha)
        return img

    def resize(self, img, spec):
        """
        - Resize icon to given size
        """
        img = img.resize((spec["size"], spec["size"]), Image.ANTIALIAS)
        return img

    def process(self, file_path, file_name, spec):
        img = self.png_img.copy()
        try:
            # The order in this list matters
            for pipeline in [
                "should_crop_to_rounded",
                "should_remove_alpha",
                "size",
                "crop_height",
            ]:
                if pipeline in spec and bool(spec[pipeline]) is True:
                    img = self.method_map[pipeline](img, spec)

        except ValueError:
            pass
        finally:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            new_stream = io.BytesIO()
            img.save(new_stream, format="PNG")
            self.path_stream_tuples.append((file_path + "/" + file_name, new_stream))


async def icon(origin_image_file):
    # Generate the icon.
    png_img = await convert_to_png(origin_image_file)

    path_stream_tuples = walk_spec("/icons", png_img)

    zip_file = zip_images(path_stream_tuples)
    download_zip(zip_file)

    usage_log.info("Icon generated: {}".format(png_img))


def walk_spec(file_path, png_img, spec=icon_spec):
    processor = Processor(png_img)
    path_stream_tuples = []

    for k, v in spec.items():
        if isinstance(v, dict) and "size" in v:
            processor.process(file_path, k, v)
        elif isinstance(v, dict):
            new_path = file_path + "/" + k
            new_path_stream_tuples = walk_spec(new_path, png_img, v)
            path_stream_tuples = path_stream_tuples + new_path_stream_tuples

    path_stream_tuples = path_stream_tuples + processor.path_stream_tuples
    return path_stream_tuples


def zip_images(path_stream_tuples):
    zip_file_bytes_io = io.BytesIO()
    with zipfile.ZipFile(zip_file_bytes_io, "w") as zip_file:
        for image_name, bytes_stream in path_stream_tuples:
            zip_file.writestr(image_name, bytes_stream.getvalue())

    # Create a ZIP file from the zip file data
    zip_file = File.new(
        [Uint8Array.new(zip_file_bytes_io.getvalue())], {"type": "application/zip"}
    )

    return zip_file


def download_zip(zip_file):
    # Create a URL for the ZIP object
    zip_url = window.URL.createObjectURL(zip_file)

    # Create a download link
    download_link = document.createElement("a")
    download_link.href = zip_url
    download_link.download = "icons.zip"
    download_link.click()


async def convert_to_png(origin_image):
    # Get the data from the files arrayBuffer as an array of unsigned bytes
    array_buf = Uint8Array.new(await origin_image.arrayBuffer())

    # BytesIO wants a bytes-like object, so convert to bytearray first
    bytes_list = bytearray(array_buf)
    origin_bytes = io.BytesIO(bytes_list)

    # Create PIL image from np array
    my_image = Image.open(origin_bytes)

    my_stream = io.BytesIO()
    my_image.save(my_stream, format="PNG")

    return my_image
