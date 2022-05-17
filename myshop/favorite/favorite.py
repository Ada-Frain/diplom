from django.conf import settings
from shop.models import Product
from decimal import Decimal

class Favorite(object):

    def __init__(self, request):
        """
        Инициализируем избранное
        """
        self.session = request.session
        favorite = self.session.get(settings.FAVORITE_SESSION_ID)
        if not favorite:
            # save an empty favorite in the session
            favorite = self.session[settings.FAVORITE_SESSION_ID] = {}
        self.favorite = favorite

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт
        """
        product_id = str(product.id)
        if product_id not in self.favorite:
            self.favorite[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if update_quantity:
            self.cafavoritert[product_id]['quantity'] = quantity
        else:
            self.favorite[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии favorite
        self.session[settings.FAVORITE_SESSION_ID] = self.favorite
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара
        """
        product_id = str(product.id)
        if product_id in self.favorite:
            del self.favorite[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов и получение продуктов из базы данных.
        """
        product_ids = self.favorite.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.favorite[str(product.id)]['product'] = product

        for item in self.favorite.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров
        """
        return sum(item['quantity'] for item in self.favorite.values())

    def len(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item["quantity"] for item in self.favorite.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                self.favorite.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.FAVORITE_SESSION_ID]
        self.session.modified = True