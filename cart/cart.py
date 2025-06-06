from products.models import Product
from django.contrib import messages
from django.utils.translation import gettext as _


class Cart:
    def __init__(self, request):
        """
        Initializes the cart with the request object and session.
        """
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
        Add the specified product to the cart with the given quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        messages.success(self.request, _('Product %s added to cart.') %product.title)


    def remove(self, product):
        """
        Remove the specified product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Marks the session as modified to ensure it is saved.
        """
        self.session.modified = True

    def __iter__(self):
        """
        Iterates over the items in the cart and retrieves product details.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Clears the cart.
        """
        del self.session['cart']
        self.save()

    def get_total_price(self):
        """
        Calculates the total price of the items in the cart.
        """
        return sum(item['product_obj'].price * item.get('quantity', 0) for item in self)
