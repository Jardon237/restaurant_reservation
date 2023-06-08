from datetime import datetime
import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from restaurant.models import ReservationSetting

from restaurant.views import SetReservations
from .models import MenuItem, Category, OrderModel, Resevations
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/landing.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class MenuPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/menu.html')


class CancelOrder(View):
    def post(self, request, *args, **kwargs):
        order_id = request.POST['order_id']
        orders = OrderModel.objects.filter(pk=order_id)
        if (orders != None):
            orders.delete()
            messages.success(request, 'order successful cancel')
            return render(request, 'customer/dashboard.html')
        return render(request, 'customer/dashboard.html')


class PlaceOrder(View):
    def get(selfl, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(
            category__name__contains='Appetizer')
        # entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            # 'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class ReservationPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/reservation.html')


class CancelReservation(View):
    def post(self, request, *args, **kwargs):
        reservation_id = request.POST['reservation_id']
        reservation = Resevations.objects.filter(pk=reservation_id)
        if (reservation != None):
            reservation.delete()
            reservations = Resevations.objects.all()
            messages.success(request, 'reservation successful cancelled')
            return redirect('dashboard')
        return redirect('dashboard')



class MakeReservation(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        number_of_seats = request.POST.get('number_of_seats')
        date = request.POST.get('date')
        Resevation_time = request.POST.get('time')

        total_number_of_reservations_set_for_given_day = ReservationSetting.objects.filter(date=date).count()
        reservations_made_given_date = Resevations.objects.filter(date=date).count()

        if(total_number_of_reservations_set_for_given_day <= reservations_made_given_date):
            messages.error(request, 'sorry, there are no more available spaces'+date)
            return redirect('index')
        
        reservation = Resevations.objects.create(
            name=name,
            email=email,
            contact=contact,
            number_of_seats=number_of_seats,
            date=date,
            Resevation_time=Resevation_time
        )

        # After everything is done, send confirmation email to the user
        body = ('Thank you for your reservation! We will do well to make sure your reservation is set before you come!\n')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        return redirect('index')
