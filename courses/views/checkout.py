from django.shortcuts import render , redirect
from courses.models import Course , Payment , UserCourse,CouponCode
from django.shortcuts import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from time import time
import logging
import razorpay

client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
logger = logging.getLogger()

@login_required(login_url='/login')
def checkout(request , slug):
    course = Course.objects.get(slug  = slug)
    user = request.user
    action = request.GET.get('action')
    couponcode = request.GET.get("couponcode")
    coupon_code_message = None  
    coupon = None
    order = None
    payment = None
    error = None
    try:
        user_course = UserCourse.objects.get(user = user  , course = course)
        error = "You are Already Enrolled in this Course"
    except:
        pass
    amount=None
    if error is None : 
        amount =  int((course.price - ( course.price * course.discount * 0.01 )) * 100)
    
    if couponcode:
        try:
            coupon = CouponCode.objects.get(course=course,code = couponcode)
            amount =  int((course.price - ( course.price * coupon.discount * 0.01 ))*100)
            # print(coupon.discount)
        except:
            coupon_code_message ="Invalid Coupan Code"
            print("coupon code invalid")

    if amount==0:
        userCourse = UserCourse(user = user , course = course)
        userCourse.save()
        return redirect('my-courses')   
    

    if action == 'create_payment':

            currency = "INR"
            notes = {
                "email" : user.email, 
                "name" : f'{user.first_name} {user.last_name}'
            }
            reciept = f"codewithvirendra-{int(time())}"
            order = client.order.create(
                {'receipt' :reciept , 
                'notes' : notes , 
                'amount' : amount ,
                'currency' : currency
                }
            )

            payment = Payment()
            payment.user  = user
            payment.course = course
            payment.order_id = order.get('id')
            payment.save()
    

    context = {
        "course" : course , 
        "order" : order, 
        "payment" : payment, 
        "user" : user , 
        "error" : error,
        "coupon" : coupon,
        "coupon_code_message" : coupon_code_message,
    }
    return  render(request , template_name="check_out.html" , context=context )    


@login_required(login_url='/login')
@csrf_exempt
def verifyPayment(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        logger.info(data)
        print(data)
        try:
            logger.info("trying verify payment")
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            logger.info(razorpay_order_id,razorpay_payment_id)
            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id  = razorpay_payment_id
            payment.status =  True
            
            userCourse = UserCourse(user = payment.user , course = payment.course)
            userCourse.save()
            logger.info("UserCourse" ,  userCourse.id)

            print("UserCourse" ,  userCourse.id)

            payment.user_course = userCourse
            payment.save()

            return redirect('my-courses')   

        except:
            return HttpResponse("Invalid Payment Details")
        
        
 