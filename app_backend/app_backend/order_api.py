from django.http import HttpResponse
from DbModel.models import User, Order, OrderToUser
from django.views.decorators import csrf
import json
import time
import copy


# url: /orders?limit=x&campus=x
def fetch_orders(request):
    request.encoding = 'utf-8'

    if 'limit' in request.GET and 'campus' in request.GET:
        limit = int(request.GET['limit'])
        _campus = int(request.GET['campus'])

        result_list = Order.objects.filter(state=0, campus=_campus).order_by("id")[0:limit]

        total = len(result_list)
        metadata_obj = {'type': 'orders', 'total': total, 'valid': True}
        order_arr = []

        crt_order_obj = {}
        for crt_order in result_list:
            crt_order_obj['order_id'] = crt_order.id
            crt_order_obj['type'] = crt_order.type
            crt_order_obj['campus'] = crt_order.campus
            crt_order_obj['title'] = crt_order.title
            crt_order_obj['description'] = crt_order.description
            crt_order_obj['crt_num'] = crt_order.current_num
            crt_order_obj['max_num'] = crt_order.max_num
            crt_order_obj['reward'] = float(crt_order.reward)
            order_arr.append(copy.deepcopy(crt_order_obj))

        return_obj = {'metadata': metadata_obj, 'orders': order_arr}
        return_json_data = json.dumps(return_obj)
    # If the client did not provide with limit
    # Return error message
    else:
        metadata_obj = {'type': 'orders', 'total': 0, 'valid': False}
        return_obj = {'metadata': metadata_obj, 'err_msg': "No limit attribute."}
        return_json_data = json.dumps(return_obj)

    print("debug" + return_json_data)
    return HttpResponse(return_json_data)


# Get a specific order in detail
# url /specific?order_id=x
def fetch_specific_order(request):
    request.encoding = 'utf-8'

    if 'order_id' in request.GET:
        order_id = request.GET['order_id']
        order_in_db = Order.objects.get(id=order_id)
        user_of_order = order_in_db.ordertouser_set.all()[0]

        result_obj = {
            'order_id': order_in_db.id,
            'type': order_in_db.type,
            'campus': order_in_db.campus,
            'title': order_in_db.title,
            'description': order_in_db.description,
            'detail': order_in_db.detail,
            'current_num': order_in_db.current_num,
            'max_num': order_in_db.max_num,
            'reward': float(order_in_db.reward),
            'user_id': user_of_order.user_id.id,
            'user_name': user_of_order.user_id.name
        }
        metadata_obj = {'type': 'specific', 'total': 1, 'valid': True}

        return_obj = {'metadata': metadata_obj, 'order_info': result_obj}
        return_json_data = json.dumps(return_obj)

        return HttpResponse(return_json_data)
    else:
        metadata_obj = {'type': 'specific', 'total': 0, 'valid': False}
        return_obj = {'metadata': metadata_obj, 'err_msg': "No id specified."}
        return_json_data = json.dumps(return_obj)

        return HttpResponse(return_json_data)


# url /new_order
def new_order(request):
    request.encoding = 'utf-8'

    order_type = request.POST['order_type']
    order_campus = request.POST['order_campus']
    order_title = request.POST['order_title']
    order_description = request.POST['order_description']
    order_detail = request.POST['order_detail']
    order_max_num = request.POST['order_max_num']
    order_reward = request.POST['order_reward']
    order_start_time = time.time()

    crt_order = Order(
        type=order_type, campus=order_campus, title=order_title,
        description=order_description, detail=order_detail, max_num=order_max_num,
        reward=order_reward, start_time=order_start_time
    )
    crt_order.save()

    order_user_id = request.POST['order_user_id']
    crt_order_user = User.objects.get(id=order_user_id)
    crt_order_to_user = OrderToUser(user_id=crt_order_user, order_id=crt_order)
    crt_order_to_user.save()

    return HttpResponse("Success")


# url /order_plus?order_id=x
def order_plus(request):
    request.encoding = 'utf-8'

    order_order_id = request.GET['order_id']
    crt_order = Order.objects.get(id=order_order_id)

    crt_order.current_num = crt_order.current_num+1
    if crt_order.current_num == crt_order.max_num:
        crt_order.state = 1

    crt_order.save()

    return HttpResponse("Success")


# url /order_done?order_id=x
def order_done(request):
    request.encoding = 'utf-8'

    order_order_id = request.GET['order_id']
    crt_order = Order.objects.get(id=order_order_id)

    crt_order.state = 2
    crt_order.end_time = time.time()

    crt_order.save()

    return HttpResponse("Success")


