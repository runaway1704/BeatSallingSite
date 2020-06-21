from decimal import Decimal
from django.conf import settings
from Beat.models import Beat


class Cart(object):
    """class for cart"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, beat):
        """add item to cart"""
        beat_id = str(beat.id)
        if beat_id not in self.cart:
            self.cart[beat_id] = {'price': str(beat.price)}
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, beat):
        """delete item from cart"""
        beat_id = str(beat.id)
        if beat_id in self.cart:
            del self.cart[beat_id]
            self.save()

    def __iter__(self):
        """iterate over objects in the cart"""
        beat_ids = self.cart.keys()
        beats = Beat.objects.filter(id__in=beat_ids)
        for beat in beats:
            self.cart[str(beat.id)]["beat"] = beat
        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            yield item

    def __len__(self):
        return sum(item for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"] for item in self.cart.values()))

    def clear(self):
        """delete cart from session"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
