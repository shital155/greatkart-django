# from django.shortcuts import render,redirect,get_object_or_404
# from store.models import Product,Variation
# from .models import Cart, CartItem
# from django.core.exceptions import ObjectDoesNotExist
#
#
#
#
# # Create your views here.
# from django.http import HttpResponse
# #
# # def _cart_id(request):
# #     if not request.session.session_key:
# #         request.session.create()
# #     return request.session.session_key
# #
# #
# # def add_cart(request, product_id):
# #     product = get_object_or_404(Product, id=product_id)
# #     product_variation = []
# #
# #     if request.method == 'POST':
# #         for key, value in request.POST.items():
# #             try:
# #                 variation = Variation.objects.get(
# #                     product=product,
# #                     variation_category__iexact=key,
# #                     variation_value__iexact=value
# #                 )
# #                 product_variation.append(variation)
# #             except:
# #                 pass
# #
# #     cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
# #
# #     cart_items = CartItem.objects.filter(product=product, cart=cart)
# #
# #     if cart_items.exists():
# #         for item in cart_items:
# #             if set(item.variations.all()) == set(product_variation):
# #                 item.quantity += 1
# #                 item.save()
# #                 break
# #         else:
# #             cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
# #             if product_variation:
# #                 cart_item.variations.set(product_variation)
# #             cart_item.save()
# #     else:
# #         cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
# #         if product_variation:
# #             cart_item.variations.set(product_variation)
# #         cart_item.save()
# #
# #     return redirect('cart')
#
#
#
#
#
#
#
#
#
#
#
#
#
# def _cart_id(request):
#     cart=request.session.session_key
#     if not cart:
#         cart=request.session.create()
#     return cart
# def add_cart(request,product_id):
#     product=Product.objects.get(id=product_id)
#     product_variation = []
#     if request.method == 'POST':
#         for item in request.POST:
#             key = item
#             value = request.POST[key]
#             try:
#                 variation =Variation.objects.get(product=product, variation_category__iexact=key,variation_value__iexact=value)
#                 product_variation.append(variation)
#             except:
#                 pass
#
#         # color=request.POST['color']
#         # size=request.POST['size']
#         # print(color, size)
#
#
#
#
#
#     try:
#         cart=Cart.objects.get(cart_id=_cart_id(request))
#     except Cart.DoesNotExist:
#         cart=Cart.objects.create(
#            cart_id=_cart_id(request)
#         )
#     cart.save()
#
#     is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
#     if is_cart_item_exists:
#         cart_item=CartItem.objects.filter(product=product,  cart=cart)
#         ex_var_list = []
#         id=[]
#         for item in cart_item:
#             existing_variation = item.variations.all()
#             ex_var_list.append(list(existing_variation))
#             id.append(item.id)
#         print(ex_var_list)
#
#         if product_variation in ex_var_list:
#             index= ex_var_list.index(product_variation)
#             item_id = id[index]
#             item=CartItem.objects.get(product=product, id=Item_id)
#             item.save()
#         else:
#             item=CartItem.objects.create(product=product, quantity=1, cart=cart)
#
#             if len(product_variation) > 0:
#                 item.variations.clear()
#
#                 item.variations.add(*product_variation)
#             item.save()
#
#         # cart_item.quantity += 1
#
#
#       else:
#         cart_item= CartItem.objects.create(
#               product= product,
#               quantity= 1,
#               cart= cart,
#         )
#         if len(product_variation) > 0:
#               cart_item.variations.clear()
#
#               cart_item.variations.add(*product_variation)
#         cart_item.save()
#
#        return redirect('cart')
#
# def remove_cart_item(request,product_id):
#     cart=Cart.objects.get(cart_id=_cart_id(request))
#     product=get_object_or_404(Product, id=product_id)
#     cart_item=CartItem.objects.get(product=product, cart=cart)
#     cart_item.delete()
#     return redirect('cart')
#
# # def remove_cart_item(request, cart_item_id):
# #     cart_item = get_object_or_404(CartItem, id=cart_item_id)
# #     cart_item.delete()
# #     return redirect('cart')
#
#
#
#
#
#
# def remove_cart(request, product_id):
#     cart=Cart.objects.get(cart_id=_cart_id(request))
#     product=get_object_or_404(Product, id=product_id)
#     cart_item= CartItem.objects.get(product=product, cart=cart)
#     if cart_item.quantity >1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart')
#
#
#
# def cart(request,total=0,quantity=0, cart_items=None):
#     try:
#         tax=0
#         grand_total=0
#         cart=Cart.objects.get(cart_id=_cart_id(request))
#         cart_items=CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass
#
#     context = {
#        'total': total,
#        'quantity': quantity,
#        'cart_items': cart_items,
#        'tax' : tax,
#        'grand_total' : grand_total,
#     }
#     return render(request, 'store/cart.html',context)


from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    # 1️⃣ Get selected variations
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # 2️⃣ Logged-in user cart
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(product=product, user=request.user)

        if cart_items.exists():
            for item in cart_items:
                if set(item.variations.all()) == set(product_variation):
                    item.quantity += 1
                    item.save()
                    return redirect('cart')

        cart_item = CartItem.objects.create(
            product=product,
            user=request.user,
            quantity=1
        )
        if product_variation:
            cart_item.variations.set(product_variation)
        cart_item.save()

    # 3️⃣ Guest user cart (session based)
    else:
        cart, _ = Cart.objects.get_or_create(cart_id=request.session.session_key)

        cart_items = CartItem.objects.filter(product=product, cart=cart)

        if cart_items.exists():
            for item in cart_items:
                if set(item.variations.all()) == set(product_variation):
                    item.quantity += 1
                    item.save()
                    return redirect('cart')

        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if product_variation:
            cart_item.variations.set(product_variation)
        cart_item.save()

    return redirect('cart')


def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def remove_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

# def remove_cart(request,product_id, cart_item_id):
#     cart= Cart.objects.get(cart_id=_cart_id(request))
#     product=get_object_or_404(Product, id=product_id)
#     try:
        # if request.user.is_authenticated:
        #     cart_item=CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        # else:
        #     cart=Cart.objects.get(cart_id=cart_id(request))
        #     cart_item=CartItem.objects.get(product=product,cart=cart, id=cart_item_id)
#       cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#       if cart_item.quantity > 1:
#           cart_item.quantity -= 1
#           cart_item.save()
#       else:
#           cart_item.delete()
#     except:
#         pass
#
#
#     return redirect('cart')
#
# def remove_cart_item(request, product_id, cart_item_id):
#     cart=Cart.objects.get(cart_id=_cart_id(request))
#     product= get_object_or_404(Product, id=product_id)
      # if request.user.is_authenticated:
      #     cart_item=CartItem.objects.get(product)
#     cart_item=CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#     cart_item.delete()
#     return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:


                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request,total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:


                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html',context)
