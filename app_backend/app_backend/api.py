from django.http import HttpResponse
from DbModel.models import User, Order, OrderToUser
import json


def fetch_orders(request):
    request.encoding = 'utf-8'
    if 'limit' in request.GET:
        limit = request.GET['limit']
        result_list = Order.objects.filter(state=0).order_by("id")[0:limit-1]

        metadata_obj = {'type': 'orders', 'limit': 10}
        order_arr = []

        crt_order_obj = {}
        for crt_order in result_list:
            crt_order_obj['order_id'] = crt_order.id
            crt_order_obj['type'] = crt_order.type
            crt_order_obj['campus'] = crt_order.campus
            crt_order_obj['title'] = crt_order.title
            crt_order_obj['detail'] = crt_order.detail
            crt_order_obj['crt_num'] = crt_order.current_num
            crt_order_obj['max_num'] = crt_order.max_num
            crt_order_obj['reward'] = crt_order.reward
            order_arr.append(crt_order_obj)
    return
