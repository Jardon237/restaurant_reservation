from django.urls import path
from .views import Dashboard, SetReservations


urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('set_reservations/', SetReservations.as_view(), name='reservation_settings'),
]
