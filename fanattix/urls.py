"""fanattix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework.authtoken import views as rest_auth_views
from rest_framework.routers import DefaultRouter

from accounts.API.views import (
    UserViewSet,
    UserShortViewSet,
    UserProfileViewSet,
    CustomObtainAuthToken
)
from events.API.views import (
    EventViewSet,
    EventOccurrenceViewSet,
    get_my_events,
    get_tickets,
    search_events_by_name,
)
from tickets.API.views import (
    TicketViewSet,
    TicketDetailViewSet,
    TicketOptionViewSet,
    purchase_ticket,
    get_purchased_tickets,
)

router = DefaultRouter()
router.register('api/users', UserViewSet)
router.register('api/users-short', UserShortViewSet)
router.register('api/user-profiles', UserProfileViewSet)
router.register('api/events', EventViewSet)
router.register('api/event-occurrences', EventOccurrenceViewSet)
router.register('api/tickets', TicketViewSet)
router.register('api/ticket-detail', TicketDetailViewSet)
router.register('api/ticket-options', TicketOptionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/api-token-auth/', CustomObtainAuthToken.as_view()),
    path('api/my-events/<int:user_id>/', get_my_events, name="get_events_created"),
    path('api/get-tickets/<int:user_id>/', get_tickets, name="get_tickets"),
    path('api/purchase-ticket/', purchase_ticket, name="purchase_tickets"),
    path('api/get-purchased-tickets/<int:user_id>/', get_purchased_tickets, name="get_purchased_tickets"),
    path('api/search-events-by-name/', search_events_by_name, name="search-events-by-name"),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
