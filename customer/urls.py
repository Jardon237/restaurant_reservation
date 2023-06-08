from django.urls import path
from restaurant.views import Dashboard


urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='customer_dashboard'),
]
