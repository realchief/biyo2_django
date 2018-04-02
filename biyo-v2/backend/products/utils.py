
from io import BytesIO
from PIL import Image, ImageOps

from django.core.files.base import ContentFile
from django.core.files import File


def is_smaller(img, newsize):
    return img.size[0] > newsize[0] \
        or img.size[1] > newsize[1]


def resize_image(image, newsize, new_format='PNG'):
    # image: ImageField instance
    resample = Image.ANTIALIAS
    crop = False
    filename = '.'.join(image.file.name.split('.')[:-1]) + ".%s" % (new_format.lower())
    with Image.open(image) as img:
        file_format = img.format

        if is_smaller(img, newsize):
            factor = 1
            while img.size[0] / factor > 2 * newsize[0] \
                    and img.size[1] * 2 / factor > 2 * newsize[1]:
                factor *= 2
            if factor > 1:
                img.thumbnail(
                    (int(img.size[0] / factor),
                     int(img.size[1] / factor)),
                    resample=resample
                )

            size = newsize[0], newsize[1]
            size = tuple(int(i) if i != float('inf') else i
                         for i in size)
            if crop:
                img = ImageOps.fit(
                    img,
                    size,
                    method=resample
                )
            else:
                img.thumbnail(
                    size,
                    resample=resample
                )
        with BytesIO() as file_buffer:
            img.save(file_buffer, new_format)
            f = File(BytesIO(file_buffer.getvalue()), filename)
            return f
