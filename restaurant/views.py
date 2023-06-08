from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import OrderModel, Resevations
from restaurant.models import ReservationSetting
from django.contrib import messages


class Dashboard(View, LoginRequiredMixin, UserPassesTestMixin):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        if (request.user.is_staff):
            orders = OrderModel.objects.filter(
                created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        else:
            orders = OrderModel.objects.filter(
                created_on__year=today.year, created_on__month=today.month, email=request.user.email)

        if (request.user.is_staff):
            reservations = Resevations.objects.all()
        else:
            reservations = Resevations.objects.filter(
                email=request.user.email).all()

        # loop through the orders and add the price value
        total_revenue = 0
        for order in orders:
            total_revenue += order.price

        # pass total number of orders and total revenue into template
        context = {
            'orders': orders,
            'reservations': reservations,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        if (request.user.is_staff == True):
            return render(request, 'restaurant/dashboard.html', context)

        return render(request, 'customer/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
class SetReservations(View):
    def post(self, request, *args, **kwargs):
        number_of_tables = request.POST['number_of_tables_per_day']
        date = request.POST['date']
        reservation = ReservationSetting.objects.create(
            number_of_tables=number_of_tables,
            date=date
        )

        if(reservation != None):
            messages.success(request, 'Settings updated')
            return redirect('dashboard')
        messages.error(request, 'Sorry could not save settings')