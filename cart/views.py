from django.shortcuts import render, get_object_or_404, redirect

from products.models import Product
from .cart import Cart
from .forms import AddToCartProductForm


def cart_detail_view(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart, })


def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'])
    return redirect('cart:cart_detail')


def remove_from_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
