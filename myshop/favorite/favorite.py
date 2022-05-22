from django.conf import settings
from shop.models import Product
import copy

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

    def add(self, product):
        """
        Добавить продукт
        """
        product_id = str(product.id)
        if product_id not in self.favorite:
            self.favorite[product_id] = {}
        
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
        product_ids = self.favorite.keys()
        products = Product.objects.filter(id__in=product_ids)
        favorite = copy.deepcopy(self.favorite)
        for product in products:
            favorite[str(product.id)]['product'] = product
        for item in favorite.values():
            yield item

    def __len__(self):
        return len(self.favorite)

    def len(self):
        return len(self.favorite)