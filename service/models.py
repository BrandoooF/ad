from django.db import models
from rest_framework import pagination

# Create your models here.


class StandardPagination(pagination.PageNumberPagination):
    page_size = 8
