from django.shortcuts import render, HttpResponse, redirect
from .models import Product, Contact, Orders, OrderUpdate
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from django.http import HttpResponse, JsonResponse



# For Email Confirmation
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def index(request):

    if request.user.is_authenticated:
        order, created = Orders.objects.get_or_create(user=request.user, complete=False)
        items = order.orderupdate_set.all()
        cartItems = order.get_cart_items
        products = Product.objects.all()
        context = {'items':items, 'cartItems':cartItems,'products':products}
        return render(request, 'app/index.html', context)
    else:
        msg=messages.warning(request, 'You are not logged in, Please login to continue')
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        products = Product.objects.all()
        context={'cartItems':cartItems, 'msg':msg, 'products':products}
        return render(request, 'app/index.html', context)
    
    return render(request, 'app/index.html')



def productView(request, myid):

    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        items = order.orderupdate_set.all()
        cartItems = order.get_cart_items
        product = Product.objects.filter(id=myid)
        context = {'cartItems':cartItems, 'product':product}
        return render(request, 'app/prodview.html', context) 
    
    else:
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        product = Product.objects.filter(id=myid)
        context = {'cartItems':cartItems, 'product':product}
        return render(request, 'app/prodview.html', context) 

    
def cart(request):

    if request.user.is_authenticated:   # admin
        user = request.user     #moksh
        print(user)
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        items = order.orderupdate_set.all()
        cartItems = order.get_cart_items
        context = {'order': order, 'items':items, 'cartItems':cartItems}
    
    else:
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        items = []
        context = {'items':items, 'cartItems': cartItems, 'order':order}

    return render(request, 'app/cart.html', context)

def search(request):
    if request.user.is_authenticated:
        order, created = Orders.objects.get_or_create(user=request.user, complete=False)
        items = order.orderupdate_set.all()
        cartItems = order.get_cart_items

        if request.method=='GET':
            query = request.GET['search']
            
            if query=='':
                order, created = Orders.objects.get_or_create(user=request.user, complete=False)
                items = order.orderupdate_set.all()
                cartItems = order.get_cart_items
                context = {'items':items, 'cartItems':cartItems,'query':query}
                return render(request, 'app/search.html', context)

            filterproduct = Product.objects.filter(product_name__icontains=query)
            context = {'filterproduct': filterproduct, 'query':query,'cartItems':cartItems}
            return render(request, "app/search.html",context)
            

    else:
        msg=messages.error(request, 'You are not logged in, Please login to continue')
       
        if request.method=='GET':
            query = request.GET['search']

            if query=='':
                order = {'get_cart_total':0, 'get_cart_items':0}
                cartItems = order['get_cart_items']
                context={'cartItems':cartItems, 'msg':msg}
                return render(request, 'app/search.html', context)
            
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']
            filterproduct = Product.objects.filter(product_name__icontains=query)
            context = {'filterproduct': filterproduct, 'query':query,'cartItems':cartItems, 'msg':msg}
        return render (request, 'app/search.html', context)

    msg = messages.info(request, 'Your search returned no results')
    return render(request, 'app/search.html',{ 'items':items, 'cartItems':cartItems, 'msg':msg})

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 10:
           messages.error(request, "Username must be under 10 characters")
           return redirect('home')

        if not username.isalnum():
           messages.error(request, "Username should only contain letters and numbers")
           return redirect('home')

        if pass1 != pass2: 
           messages.error(request, "Passwords do not match")
           return redirect('home')            

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        name = fname + ' ' + lname
        myuser.save()
        context = {'name':name, 'email':email, 'username':username, 'pass1':pass1}
        template = render_to_string('app/signup_template.html',context)
        email = EmailMessage('Your account has been created',template, settings.EMAIL_HOST_USER,[email])
        email.fail_silently = False
        email.send()
        print("Email sent")
        messages.success(request, "Your Bizzare account has been successfully created")
        return redirect('home')
    else:
        msg="Please fill the form"
        return render(request, 'app/signup.html', {'msg':msg})

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try agin")
            return redirect('home')
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

def about(request):

    if request.user.is_authenticated:
        order, created = Orders.objects.get_or_create(user=request.user, complete=False)
        items = order.orderupdate_set.all()
        cartItems = order.get_cart_items
        context={'items':items, 'cartItems':cartItems}
    else:
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        context = {'cartItems':cartItems}
        return render(request, 'app/about.html',context) 

    return render(request, 'app/about.html',context)


def contact(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        items = order.orderupdate_set.all()
        cartItems = order.get_cart_items
        context= {'cartItems':cartItems}


        if request.method=="POST":
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            desc = request.POST.get('desc', '')
            print(name, email, phone,desc)

            if len(name)<10 or len(email)<10 or len(phone)<10 or len(desc)<10:
                messages.error(request, "Please fill the form correctly")
            else:
                contact = Contact(name=name, email=email, phone=phone, desc=desc)
                contact.save()
                messages.success(request, "Your message has been successfully sent")
                context= {'cartItems':cartItems}
                return render (request, 'app/contact.html', context)
       
    else:
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        context= {'cartItems':cartItems}
        msg=messages.error(request, "Please login to continue")
        context= {'cartItems':cartItems, 'msg':msg}
        return render(request, 'app/contact.html', context)
    
    return render (request, 'app/contact.html',context)



def checkout(request):

    if request.user.is_authenticated:
        order, created = Orders.objects.get_or_create(user=request.user)
        cartItems = order.get_cart_items

        context = {'cartItems':cartItems,'order':order}

        if request.method=="POST":
            order = Orders.objects.get(user=request.user)
            name = request.POST.get('name', '')
            amount = request.POST.get('amount', '')
            amount = order.get_cart_total
            email = request.POST.get('email', '')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')
            if cartItems == 0:
                messages.error(request, "Your cart is empty")
                return redirect('checkout')
            if name == '' or email == '' or address == '' or city == '' or state == '' or zip_code == '' or phone == '':
                msg = messages.error(request, "Please fill the form correctly")
                redirect('checkout')
            else:
                order = Orders( order_id=order.order_id,name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount, complete=True)
                order.save()
                print(order)

                param_dict = {
                    'MID': 'LQtwtj60370135811954',
                    'ORDER_ID': str(order.order_id),
                    'TXN_AMOUNT': str(amount),
                    'CUST_ID': email,
                    'INDUSTRY_TYPE_ID': 'Retail',
                    'WEBSITE': 'WEBSTAGING',
                    'CHANNEL_ID': 'WEB',
                    'CALLBACK_URL':'http://127.0.0.1:8000/app/handlerequest/',
                }
                MERCHANT_KEY = '9&s27MJiTSfIEeQ9'
                param_dict['CHECKSUMHASH'] = Checksum.generateSignature(param_dict, MERCHANT_KEY)
                return  render(request, 'app/paytm.html', {'param_dict': param_dict})

    else:
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        context= {'cartItems':cartItems}
        msg=messages.warning(request, "Please login to checkout")
        context= {'cartItems':cartItems, 'msg':msg}
        return render(request, 'app/checkout.html', context)

    return render(request, 'app/checkout.html',context) 

@csrf_exempt
def handlerequest(request):

    #paytm will send you post request here
    MERCHANT_KEY = '9&s27MJiTSfIEeQ9'

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]


    verify = Checksum.verifySignature(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            
            print('order successful')
            template = render_to_string('app/email_template.html', {'name':Orders.objects.get(order_id=response_dict['ORDERID']).name, 'link':'http://127.0.0.1:8000/tracker/', 'order_id':Orders.objects.get(order_id=response_dict['ORDERID']).order_id})
            email = EmailMessage('Thank You for purhasing for our store',template, settings.EMAIL_HOST_USER, [Orders.objects.get(order_id=response_dict['ORDERID']).email])
            email.fail_silently = False
            email.send()
            print("Email sent")
        else:
            print('order was not successful because' + response_dict['RESPMSG'])

    return render(request, 'app/paymentstatus.html', {'response': response_dict})



def tracker(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        items = order.orderupdate_set.all()
        cartItems = order.get_cart_items
        context={'items':items, 'cartItems':cartItems}

        if request.method=="POST":
            orderId = request.POST.get('orderId', '')
            oemail = request.POST.get('oemail', '')
            try:
                order = Orders.objects.filter(order_id=orderId, email=oemail)
                if len(order)>0:
                    update = OrderUpdate.objects.filter(order=orderId)
                    msg=messages.info(request, "Order matching to your order id has been found")
                    order, created = Orders.objects.get_or_create(user=user, complete=False)
                    
                    items = order.orderupdate_set.all()
                    cartItems = order.get_cart_items
                    context= {'order': order, 'items':items, 'cartItems':cartItems, 'update':update}
                    return render(request, 'app/tracker.html', context)
                else:
                    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
                    cartItems = order['get_cart_items']
                    context = {'order':order, 'cartItems':cartItems}
                    msg=messages.error(request, "Sorry, No order found to your order id")
                    context= {'cartItems':cartItems, 'msg':msg}
                    return render(request, 'app/tracker.html', context)
                
            except Exception as e:
                return HttpResponse('<strong>404 Not Found </strong>')

    else:
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        context= {'cartItems':cartItems}
        msg=messages.error(request, "Please login to track your order")
        context= {'cartItems':cartItems, 'msg':msg}
        return render(request, 'app/tracker.html', context)

    return render(request, 'app/tracker.html',context) 

def men(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        cartItems = order.get_cart_items
        context = {'cartItems':cartItems}
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        context = {'order':order, 'cartItems':cartItems}


    products = Product.objects.filter(category='Men')
    context = {'cartItems':cartItems,'order':order,'products':products}
    return render(request,'app/pages.html', context)

def women(request):

    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        cartItems = order.get_cart_items
        context = {'cartItems':cartItems,'order':order}

    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        context = {'order':order, 'cartItems':cartItems}

    products = Product.objects.filter(category='Women')
    context = {'cartItems':cartItems,'order':order,'products':products}
    return render(request,'app/pages.html', context)

def footwear(request):
    
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        cartItems = order.get_cart_items
        context={'cartItems':cartItems,'order':order}

    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        context = {'order':order, 'cartItems':cartItems}

    products = Product.objects.filter(category='Footwear')
    context = {'cartItems':cartItems,'order':order,'products':products}
    return render(request,'app/pages.html', context)

def furniture(request):
    
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        cartItems = order.get_cart_items
        context={'cartItems':cartItems,'order':order}

    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        context = {'order':order, 'cartItems':cartItems}

    products = Product.objects.filter(category='Furniture')
    context = {'cartItems':cartItems,'order':order,'products':products}
    return render(request,'app/pages.html', context)

def homeDecor(request):
    
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        cartItems = order.get_cart_items
        context={'cartItems':cartItems,'order':order}

    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        context = {'order':order, 'cartItems':cartItems}

    products = Product.objects.filter(category='Home-Decor')
    context = {'cartItems':cartItems,'order':order,'products':products}
    return render(request,'app/pages.html', context)

def accessories(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, complete=False)
        cartItems = order.get_cart_items
        context={'cartItems':cartItems,'order':order}

    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        context = {'order':order, 'cartItems':cartItems}

    products = Product.objects.filter(category='Accessories')
    context = {'cartItems':cartItems,'order':order,'products':products}
    return render(request,'app/pages.html', context)

def updateItem(request):
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']


    print('Action:', action)
    print('Product:', productId)

    user = request.user
    print(user)
    product = Product.objects.get(product_id=productId)
    order, created = Orders.objects.get_or_create(user=user, complete=False) 
    orderUpdate, created = OrderUpdate.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderUpdate.quantity = (orderUpdate.quantity + 1)
    elif action == 'remove':
        orderUpdate.quantity = (orderUpdate.quantity - 1)
    orderUpdate.save()


    if orderUpdate.quantity <=0:
        orderUpdate.delete()

    return JsonResponse("item added to cart", safe=False)
