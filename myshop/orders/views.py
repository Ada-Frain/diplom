from email import message
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            id = order.id
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            postal_code = form.cleaned_data['postal_code']
            created = order.created
            updated = order.updated
            status = form.cleaned_data['status']
            message_for_client = f'Здравствуйте, {first_name} {last_name}.\n\nВаш заказ успешно оформлен. Номер вашего заказа {id}. Вы выбрали способ доставки {status}. Мы свяжемся с вами в ближайшее время для подтверждения заказа.\n\nС уважением, администрация магазина Пикачу.'
            message_for_admin = f'Номер заказа: {id}\nИмя: {first_name}\nФамилия: {last_name}\nПочта: {email}\nАдрес: {address}\nИндекс: {postal_code}\nСоздано: {created}\nОбновлено: {updated}\nФорма доставки: {status}'
            try:
                send_mail('Спасибо за покупку!', message_for_client, settings.EMAIL_HOST_USER, [f'{email}'])
                send_mail(f'Заказ №{id}', message_for_admin, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # очистка корзины
            cart.clear()
            return render(request, "orders/order/created.html", {"order": order})
    else:
        form = OrderCreateForm
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})