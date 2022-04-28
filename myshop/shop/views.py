from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Category, Fandom, Product
from cart.forms import CartAddProductForm
from .forms import FavoritesAddProductForm


def fandom_list(request, fandom_slug=None):
    categories = Category.objects.all()
    fandom = None
    fandoms = Fandom.objects.all()
    products = Product.objects.filter(available=True)
    if fandom_slug:
        fandom = get_object_or_404(Fandom, slug=fandom_slug)
        products = products.filter(fandom=fandom)
    return render(
        request,
        "shop/product/fandoms.html",
        {"categories": categories, "fandom": fandom, "fandoms": fandoms, "products": products},
    )


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = None
    results = []

    if request.GET.get("search"):
        query = request.GET["search"]
        results = Product.objects.filter(name__iregex=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(
        request,
        "shop/product/list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "query": query,
            "results": results,
        },
    )


def product_detail(request, id, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        "shop/product/detail.html",
        {"categories": categories, "product": product, "cart_product_form": cart_product_form},
    )


def about(request):    
    categories = Category.objects.all()
    return render(request, "shop/information/about.html", {"categories": categories})

def delivery(request):    
    categories = Category.objects.all()
    return render(request, "shop/information/delivery.html", {"categories": categories})

def contacts(request):    
    categories = Category.objects.all()
    return render(request, "shop/information/contacts.html", {"categories": categories})

def discounts(request):    
    categories = Category.objects.all()
    return render(request, "shop/information/discounts.html", {"categories": categories})


