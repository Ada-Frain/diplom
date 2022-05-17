from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from .models import Category, Fandom, Product, Rating
from cart.forms import CartAddProductForm
from .forms import FavoritesAddProductForm, RatingForm
import operator


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
    ordered = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = None
    results = []
    print(products)

    if request.GET.get("search"):
        query = request.GET["search"]
        results = Product.objects.filter(name__iregex=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        ordered = sorted(products, key=operator.attrgetter('name'))
        print(products)

    return render(
        request,
        "shop/product/list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "query": query,
            "results": results,
            "ordered": ordered
        },
    )


def product_detail(request, id, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    rating_stars = Rating.objects.filter(product=product).values('star')
    print(rating_stars)
    cart_product_form = CartAddProductForm()
    favorite_product_form = FavoritesAddProductForm()
    star_form = RatingForm()
    sum = 0
    for elem in rating_stars:
        sum += elem.get('star', None)
    if sum != 0:
        avg = round(float(sum/len(rating_stars)), 2)
    else:
        avg = 0
    return render(
        request,
        "shop/product/detail.html",
        {"categories": categories, "product": product, "cart_product_form": cart_product_form, "favorite_product_form": favorite_product_form, "star_form": star_form, "avg": avg},
    )


@require_POST
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_rating(request):
    form = RatingForm(request.POST)
    if form.is_valid():
        Rating.objects.update_or_create(
            ip=get_client_ip(request),
            product_id=int(request.POST.get("product")),
            defaults={'star_id': int(request.POST.get("star"))}
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse(status=400)



