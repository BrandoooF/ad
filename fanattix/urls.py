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
from django.urls import path, include
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
    CategoryViewSet,
    TypeViewSet,
    get_my_events,
    get_tickets,
    search_events_by_name,
    search_events_by_CLD,
    send_email_to_patrons,
    get_free_events,
    get_events_by_category,
    get_events_nearby,
    filter_events
)
from tickets.API.views import (
    TicketViewSet,
    TicketDetailViewSet,
    TicketOptionViewSet,
    TicketOptionDetailViewSet,
    purchase_ticket,
    get_purchased_tickets,
    check_in
)

from stripeservice.API.views import (
    get_connect_user_info,
    charge,
    save_card,
    StripeSavedPaymentMethodViewSet,
    get_payment_methods,
    StripeConnectedUserViewSet,
    get_connected_user,
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
router.register('api/ticket-option-detail', TicketOptionDetailViewSet)
router.register('api/categories', CategoryViewSet)
router.register('api/types', TypeViewSet)
router.register('api/payment-methods', StripeSavedPaymentMethodViewSet)
router.register('api/connect-accounts', StripeConnectedUserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/api-token-auth/', CustomObtainAuthToken.as_view()),
    path('api/my-events/<int:user_id>/', get_my_events, name="get_events_created"),
    path('api/get-tickets/<int:user_id>/', get_tickets, name="get_tickets"),
    path('api/purchase-ticket/', purchase_ticket, name="purchase_tickets"),
    path('api/get-purchased-tickets/<int:user_id>/', get_purchased_tickets, name="get_purchased_tickets"),
    path('api/search-events-by-name/', search_events_by_name, name="search-events-by-name"),
    path('api/search-events-by-cld/', search_events_by_CLD, name="search-events-by-cld"),
    path('api/get-free-events/', get_free_events, name="get_free_events"),
    path('api/get-connect-user-info/', get_connect_user_info, name="get_connect_user_info"),
    path('api/charge/', charge, name="charge"),
    path('api/email-patrons/', send_email_to_patrons, name="send_email_to_patrons"),
    path('api/events-by-category/', get_events_by_category, name="send_email_to_patrons"),
    path('api/ticket-service/', include('tickets.urls')),
    path('api/save-card/', save_card, name="save_card"),
    path('api/payment-methods/<int:user_id>/', get_payment_methods, name="get_payment_methods"),
    path('api/connected-accounts/<int:user_id>/', get_connected_user, name="get_payment_methods"),
    path('api/check-ticket/<int:ticket_id>/', check_in, name="check_in"),
    path('api/events-near-location/', get_events_nearby, name="get_events_nearby"),
    path('api/filter-events/', filter_events, name="filter_events"),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
