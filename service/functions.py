import base64
from django.core.files.base import ContentFile

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def convert_and_save_image(img_data, img_name):
    img_format, imgstr = img_data.split(';base64,')  # data:image/jpeg;base64,
    ext = img_format.split('/')[-1]
    img_name = img_name.replace(" ", "-")
    img_data = ContentFile(base64.b64decode(imgstr),
                           name=img_name + "." + ext)  # You can save this as file instance.
    return img_data


def send_email_to_patrons(subject, html_message, from_email, to_email):
    subject = subject
    html_message = render_to_string('events/email-patrons.html', {'message_body': html_message})
    plain_message = strip_tags(html_message)
    from_email = 'brandon.f.fallings@gmail.com'
    to_email = to_email # to email is already a list
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)  # send the email
