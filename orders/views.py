from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order,Payment,OrderProduct
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.
#
# def payments(request):
#     body= json.loads(request.body)
      # order=Oorder.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
      # # payment=Payment(
      #   user= request.user,
          # payment_id= body['transID'],
          # payment_method= body['payment_method'],
          # amount_paid=order.order_total,
          # status=body['status'],

      # )
        # payment.save()
          # order.payment=payment
          # order.is_ordered=True
          # order.save()
            # cart_items = CartItem.objects.filter(user=request.user)
            # for item in cart_items:
            #     orderproduct= OrderProduct()
            #     orderproduct.order_id = order.# IDEA:
            #     orderproduct.payment=payment
            #     orderproduct.user_id = request.user_id
            #     orderproduct.product_id = item.product_id
            #     orderproduct.quantity= item.quantity
            #     orderproduct.product_price= item.product.Price
            #     orderproduct.ordered = True
            #     orderproduct.save()
#           return render(request, 'orders/payments.html')    # return render(request, 'orders/payments.html')

    # views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def payments(request):
#     body = json.loads(request.body)
#
#     orderID = body['orderID']
#     transID = body['transID']
#     payment_method = body['payment_method']
#     status = body['status']
#
#     # 🟢 Save payment info here
#     # Example:
#     # order = Order.objects.get(...)
#     # order.is_ordered = True
#     # order.save()
#
#     return JsonResponse({
#         'status': 'success',
#         'redirect_url': '/orders/order_complete/'
#     })
# @csrf_exempt
# def payments(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#
#         orderID = body.get('orderID')       # Django order_number
#         transID = body.get('transID')       # PayPal transaction ID
#         payment_method = body.get('payment_method')
#         status = body.get('status')
#
#         try:
#             order = Order.objects.get(order_number=orderID, is_ordered=False)
#
#             order.payment_id = transID
#             order.payment_method = payment_method
#             order.status = status
#             order.is_ordered = True
#             order.save()

#
#             return JsonResponse({
#                 'status': 'success',
#                 'redirect_url': '/orders/order_complete/'
#             })
#
#         except Order.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Order not found'})
#
#
from .models import Order, Payment

# @csrf_exempt
# def payments(request):
#     if request.method == "POST":
#         try:
#             body = json.loads(request.body)
#
#             orderID = body.get('orderID')
#             transID = body.get('transID')
#             payment_method = body.get('payment_method')
#             status = body.get('status')
#
#             order = Order.objects.get(order_number=orderID, is_ordered=False)
#
#             # ⭐ CREATE PAYMENT ENTRY
#             payment = Payment(
#                 user=order.user,
#                 payment_id=transID,
#                 payment_method=payment_method,
#                 amount_paid=order.order_total,
#                 status=status,
#             )
#             payment.save()
#
#             # ⭐ LINK PAYMENT TO ORDER
#             order.payment = payment
#             order.is_ordered = True
#             order.status = status
#             order.save()
#
#             return JsonResponse({
#                 'status': 'success',
#                 'redirect_url': '/orders/order_complete/'
#             })
#
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
#
#     return JsonResponse({'status': 'invalid request'})
#
#
# @csrf_exempt
# def payments(request):
#     if request.method == "POST":
#         try:
#             body = json.loads(request.body)
#
#             orderID = body.get('orderID')
#             transID = body.get('transID')
#             payment_method = body.get('payment_method')
#             status = body.get('status')
#
#             order = Order.objects.get(order_number=orderID, is_ordered=False)
#
#             # 1️⃣ Create Payment
#             payment = Payment.objects.create(
#                 user=order.user,
#                 payment_id=transID,
#                 payment_method=payment_method,
#                 amount_paid=order.order_total,
#                 status=status
#             )
#
#             # 2️⃣ Link payment to order
#             order.payment = payment
#             order.is_ordered = True
#             order.status = status
#             order.save()
#
#             # 3️⃣ Move cart items → OrderProduct
#             cart_items = CartItem.objects.filter(user=order.user)
#
#             for item in cart_items:
#                order_product = OrderProduct.objects.create(
#                order=order,
#                payment=payment,
#                user=order.user,
#                product=item.product,
#                quantity=item.quantity,
#                product_price=item.product.price,
#                ordered=True
#                )
#
#             cart_variations = item.variations.all()
#             order_product.variations.set(cart_variations)
#
#
#             # 4️⃣ Clear cart
#             cart_items.delete()
#
#             return JsonResponse({
#                 'status': 'success',
#                 'redirect_url': '/orders/order_complete/'
#             })
#
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
#
#     return JsonResponse({'status': 'invalid request'})


from django.db import transaction
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
@transaction.atomic
def payments(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            orderID = body.get('orderID')
            transID = body.get('transID')
            payment_method = body.get('payment_method')
            status = body.get('status')

            order = Order.objects.select_for_update().get(
                order_number=orderID,
                is_ordered=False
            )

            payment = Payment.objects.create(
                user=order.user,
                payment_id=transID,
                payment_method=payment_method,
                amount_paid=order.order_total,
                status=status
            )

            order.payment = payment
            order.is_ordered = True
            order.status = status
            order.save()

            cart_items = CartItem.objects.filter(user=order.user)

            for item in cart_items:
                product = item.product.__class__.objects.select_for_update().get(id=item.product.id)

                if product.stock < item.quantity:
                    raise Exception(f"{product.product_name} is out of stock")

                product.stock = F('stock') - item.quantity
                product.save()

                order_product = OrderProduct.objects.create(
                    order=order,
                    payment=payment,
                    user=order.user,
                    product=product,
                    quantity=item.quantity,
                    product_price=product.price,
                    ordered=True
                )

                cart_variations = item.variations.all()
                order_product.variations.set(cart_variations)

            # 4️⃣ Clear cart
            cart_items.delete()

            # 5️⃣ SEND EMAIL (INSIDE TRY)
            order_products = OrderProduct.objects.filter(order=order)

            subject = "Thank you for your order!"
            html_message = render_to_string('orders/order_received_email.html', {
                'user': order.user,
                'order': order,
                'order_products': order_products,
            })

            email = EmailMessage(subject, html_message, to=[order.user.email])
            email.content_subtype = "html"
            email.send()



            return JsonResponse({
        'status': 'success',
        'redirect_url': f'/orders/order_complete/?order_number={order.order_number}&payment_id={payment.payment_id}'
    })


        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid request'})




# Create your views here.

def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items=CartItem.objects.filter(user=current_user)
    cart_count= cart_items.count()
    if cart_count<=0:
        return redirect('store')

    grand_total=0
    tax=0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total)/100
    grand_total = total + tax


    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city  = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total= grand_total
            data.tax= tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.is_ordered = False
            data.save()

            # generate order number

            yr = int(datetime.date.today().strftime('%Y'))
            dt= int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number=current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order=Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context= {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,

            }
            return render(request, 'orders/payments.html',context)

        else:
            return redirect('checkout')


# @login_required(login_url='login')
# def place_order(request, total=0, quantity=0):
#
#     current_user = request.user
#     cart_items = CartItem.objects.filter(user=current_user, is_active=True)
#
#     if not cart_items.exists():
#         return redirect('store')
#
#     total = 0
#     quantity = 0
#     for cart_item in cart_items:
#         total += cart_item.product.price * cart_item.quantity
#         quantity += cart_item.quantity
#
#     tax = (2 * total) / 100
#     grand_total = total + tax
#
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = Order()
#             order.user = current_user
#             order.first_name = form.cleaned_data['first_name']
#             order.last_name = form.cleaned_data['last_name']
#             order.phone = form.cleaned_data['phone']
#             order.email = form.cleaned_data['email']
#             order.address_line_1 = form.cleaned_data['address_line_1']
#             order.address_line_2 = form.cleaned_data['address_line_2']
#             order.country = form.cleaned_data['country']
#             order.state = form.cleaned_data['state']
#             order.city = form.cleaned_data['city']
#             order.order_note = form.cleaned_data['order_note']
#             order.order_total = grand_total
#             order.tax = tax
#             order.ip = request.META.get('REMOTE_ADDR')
#             order.is_ordered = True   # ⭐ CRITICAL
#             order.save()
#
#             # Order number
#             current_date = datetime.date.today().strftime("%Y%m%d")
#             order.order_number = current_date + str(order.id)
#             order.save()
#
#             # Save order products
#             for item in cart_items:
#                 OrderProduct.objects.create(
#                     order=order,
#                     user=current_user,
#                     product=item.product,
#                     quantity=item.quantity,
#                     price=item.product.price,
#                     ordered=True
#                 )
#
#             # Clear cart
#             cart_items.delete()
#
#             return redirect('order_success')
#
    return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order=order)

        subtotal=0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)

    except:
        return redirect('home')
