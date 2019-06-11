from django.urls import path
from . import views

urlpatterns = [
    path('<int:ticket_id>/', views.get_ticket, name="ticket")
]