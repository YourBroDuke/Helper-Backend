from django.http import HttpResponse
from DbModel.models import User, Order, OrderToUser
import json
import time


# url /sign_up?email=x&password=x
def user_sign_up(request):
    request.encoding = 'utf-8'

    password = request.GET['password']
    sign_up_email = request.GET['email']

    exist_email = User.objects.filter(email_address=sign_up_email)
    if exist_email.count() == 0:
        crt_user = User(name="User", hashed_password=password, email_address=sign_up_email)
        crt_user.save()
        crt_user.name = crt_user.name+str(crt_user.id)
        crt_user.save()

        user_obj = {'id': crt_user.id, 'name': crt_user.name,
                    'phone': crt_user.phone_number, 'balance': crt_user.balance}

        return_obj = {'valid': True, 'user': user_obj}

        return HttpResponse(json.dumps(return_obj))
    else:
        return_obj = {'valid': False}
        return HttpResponse(json.dumps(return_obj))


# url /log_in?email_address=x&password=x
def user_log_in(request):
    log_in_email = request.GET['email']
    password = request.GET['password']

    exist_user = User.objects.filter(email_address=log_in_email)
    if exist_user.count() == 1 and password == exist_user[0].hashed_password:

        crt_user = exist_user[0]

        user_obj = {'id': crt_user.id, 'name': crt_user.name,
                    'phone': crt_user.phone_number, 'balance': float(crt_user.balance)}
        return_obj = {'valid': True, 'user': user_obj}

        return HttpResponse(json.dumps(return_obj))
    else:
        return_obj = {'valid': False}
        return HttpResponse(json.dumps(return_obj))
