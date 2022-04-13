from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import hmac
import hashlib
import json
import razorpay
import smtplib
from email.mime.text import MIMEText


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

@csrf_exempt
def sendEmail(request):
    reqData = json.loads(request.body)
    sender = 'support@mediyush.com'
    courseName = reqData['courses'][0]['courseName']
    displayName = reqData['userDetails'][0]['displayName']
    orderId = reqData['paymentDetails']['razorpay_order_id']
    htmlBody = '''
    Hello %s, 

        Thank you for placing order with Mediyush,
        your booking order Id is %s
        Course details are -
            Course Name : %s
    
    Warm Regards,
    Mediyush
    '''%(displayName, orderId,courseName)
    recipient = reqData['userDetails'][0]['email']
    msg = (MIMEText(htmlBody))
    msg['Subject'] = "Greetings!! Your Order with Mediyush was successfully placed."
    msg['From'] = sender
    msg['To'] = recipient
    server = smtplib.SMTP_SSL('smtp.zoho.in', 465)
    server.login('support@mediyush.com', 'Support@123')
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()
    return HttpResponse('test', content_type="application/json")   