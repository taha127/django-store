from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
import requests
import json
from django.conf import settings
from django.http import HttpResponse

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10
    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': 'http://localhost:8000/',
    }
    response = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    data = response.json()['data']
    print(data)
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()
    if 'errors' not in data or len(response.json()['errors']) == 0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')
