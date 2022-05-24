from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from .models import Category, Fandom, Product, Rating, Response
from cart.forms import CartAddProductForm
from favorite.forms import FavoriteAddProductForm
from .forms import RatingForm, ResponseForm
import operator


def about(request):    
    categories = Category.objects.all()
    comments = Response.objects.filter(active=True)
    print(comments)
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            comment = form.save()
            return render(request, "shop/information/about.html", {"categories": categories, "comments": comments, "comment": comment})
    else:
        form = ResponseForm
    return render(request, "shop/information/about.html", {"categories": categories, "comments": comments, "form": form})

def delivery(request):    
    categories = Category.objects.all()
    return render(request, "shop/information/delivery.html", {"categories": categories})

def contacts(request):    
    categories = Category.objects.all()
    return render(request, "shop/information/contacts.html", {"categories": categories})

def discounts(request):    
    categories = Category.objects.all()
    return render(request, "shop/information/discounts.html", {"categories": categories})


def price_filter(request, min_price, max_price):
    categories = Category.objects.all()
    if request.method == "POST":
        min_price = request.POST.get["min_price"]
        max_price = request.POST.get["max_price"]
    
    products = Product.objects.filter(price__range=(min_price, max_price))
    return render(request, "shop/product/popular.html", {"categories": categories, "products": products},)


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

def popular_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    popular = Rating.objects.all().order_by('-star').values('product')[:6]
    ids = []
    results = []
    for elem in popular:
        ids.append(elem.get('product', None))
    products = Product.objects.filter(id__in=ids)

    if request.GET.get("min_price") and request.GET.get("max_price"):
        min_price = request.GET["min_price"]
        max_price = request.GET["max_price"]
        results = Product.objects.filter(price__range=(int(min_price), int(max_price)))
        print(min_price, max_price, results)

    return render(request, "shop/product/popular.html", {"categories": categories, "results": results, "products": products,})


def product_list(request, category_slug=None):
    category = None
    ordered = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    popular = Rating.objects.all().order_by('-star').values('product')[:6]
    ids = []
    for elem in popular:
        ids.append(elem.get('product', None))
    print(ids)
    products = Product.objects.filter(id__in=ids)
    query = None
    results = []

    if request.GET.get("search"):
        query = request.GET["search"]
        results = Product.objects.filter(name__iregex=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        ordered = sorted(products, key=operator.attrgetter('name'))

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
    cart_product_form = CartAddProductForm()
    favorite_product_form = FavoriteAddProductForm()
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



