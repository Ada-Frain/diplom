from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from shop.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, p_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=p_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"], update_quantity=cd["update"])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, p_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=p_id)
    cart.remove(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_detail(request):
    categories = Category.objects.all()
    cart = Cart(request)
    return render(request, "cart/detail.html", {"categories": categories, "cart": cart})