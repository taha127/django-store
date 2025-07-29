from django.shortcuts import render, get_object_or_404, redirect, reverse
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
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),
    }
    response = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    data = response.json()['data']
    # print(data)
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()
    if 'errors' not in data or len(response.json()['errors']) == 0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')
def payment_callback_view(request):
     payment_authority = request.GET.get('Authority')
     payment_status = request.GET.get('Status')
     order = get_object_or_404(Order, zarinpal_authority=payment_authority)
     toman_total_price = order.get_total_price()
     rial_total_price = toman_total_price * 10
     if payment_status == 'OK':
         request_header = {
             'accept': 'application/json',
             'content-type': 'application/json',
         }
         request_data = {
             'merchant_id': settings.ZARINPAL_MERCHANT_ID,
             'amount': rial_total_price,
             'authority': payment_authority,
         }
         zarinpal_verify_url = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
         response = requests.post(zarinpal_verify_url, data=json.dumps(request_data), headers=request_header)
         if 'data' in response.json()  and ('errors' not in response.json()['data'] or len(response.json()['errors']) == 0):
            data = response.json()['data']
            # print("#$%#", data)
            payment_code = data['code']
            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()
                return HttpResponse('Your payment was successful.')
            elif payment_code == 101:
                return HttpResponse('Your payment was successful. However, this transaction has already been recorded.')
            else:
                error_code = response.json()['errors']['code']
                error_message = response.json()['errors']['message']
                return HttpResponse(f'Error code: {error_code}, message: {error_message}. Transaction failed.')
     else:
        return HttpResponse('Transaction failed.')