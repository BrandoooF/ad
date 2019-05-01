import base64
from django.core.files.base import ContentFile


def convert_and_save_image(img_data, img_name):
    img_format, imgstr = img_data.split(';base64,')  # data:image/jpeg;base64,
    ext = img_format.split('/')[-1]
    img_name = img_name.replace(" ", "-")
    img_data = ContentFile(base64.b64decode(imgstr),
                           name=img_name + "." + ext)  # You can save this as file instance.
    return img_data
