from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import hmac
import hashlib
import json
import razorpay

# Create your views here.
razorpay_client = razorpay.Client(auth=("rzp_live_T09U9ZkVac10lL", "BVVuE8GoxCfSurrHH5ndDmQU"))

def hmac_sha256(val):
    h = hmac.new(razpay_secret.encode("ASCII"), val.encode("ASCII"), digestmod=hashlib.sha256).hexdigest()
    print(h)
    return h

@csrf_exempt   
def create_order(request):
    reqData = json.loads(request.body)
    currency='INR'
    razorpay_order = razorpay_client.order.create(dict(amount=reqData['amount'],
                                                    currency=currency,
                                                    payment_capture='1'))
    return HttpResponse(json.dumps(razorpay_order), content_type="application/json")
    