from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse

from .models import *

from songline import Sendline

from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User

# Create your views here.

# def home(request):
#     return HttpResponse('<h1>Hello World</h1>') 

def home(request):
    allproduct = Product.objects.all()
    context = {'pd': allproduct}
    return render(request, 'myapp/home.html', context)

def aboutUs(request):
    return render(request, 'myapp/aboutus.html')

def contact(request):
    token = 'C5Vjd8IRjdQarBR6Xeu5Dv3gD5EpJY43hbwvhLypQx4'
    context = {} #message to notify

    if request.method == 'POST':
        data = request.POST.copy()
        topic = data.get('topic')
        email = data.get('email')
        detail = data.get('detail')

        if (topic == '' or email == '' or detail == ''):
            context['message'] = 'Please, fill in all contact information'
            return render(request, 'myapp/contact.html', context)

        newRecord = contactList() #create object
        newRecord.topic = topic
        newRecord.email = email
        newRecord.detail = detail
        newRecord.save() #save data

        context['message'] = 'The message has been received'

        m = Sendline(token)
        m.sendtext('\ntopic:{0}\n email:{1}\n detail:{2}'.format(topic, email, detail))
    return render(request, 'myapp/contact.html', context)

def userLogin(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')
        password = data.get('password')

        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home-page')
        except:
            context['message'] = "username or password is incorrect."

    return render(request, 'myapp/login.html', context)

def showContact(request):
    allcontact = contactList.objects.all()
    # allcontact = contactList.object.all().order_by('-id') # reverse list
    context = {'contact': allcontact}
    return render(request, 'myapp/showcontact.html', context)

def userRegist(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repassword = data.get('repassword')

        try:
            User.objects.get(username=username)
            context['message'] = "Username duplicate"
        except:
            newuser = User()
            newuser.username = username
            newuser.first_name = firstname
            newuser.last_name = lastname
            newuser.email = email

            if (password == repassword):
                newuser.set_password(password)
                newuser.save()
                newprofile = Profile()
                newprofile.user = User.objects.get(username=username)
                newprofile.save()
                context['message'] = "register complete."
            else:
                context['message'] = "password or re-password is incorrect."

    return render(request, 'myapp/register.html', context)

def userProfile(request):
    context = {}
    userprofile = Profile.objects.get(user=request.user)
    context['project'] = userprofile
    return render(request, 'myapp/profile.html', context)

def editProfile(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        current_user = User.objects.get(id=request.user.id)
        current_user.first_name = firstname
        current_user.last_name = lastname
        current_user.username = username
        current_user.email = email
        current_user.set_password(password)
        current_user.save()

        try:
            user = authenticate(username=current_user.username,
                                password=current_user.password)
            login(request, user)
            return redirect('home-page')
        except:
            context['message'] = "edit profile fail"

    return render(request, 'myapp/editprofile.html', context)

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product, submitted=False)
    if not created:
        cart.quantity += 1
    cart.save()
    return redirect('home-page')

def cart_review(request):
    cart_items = Cart.objects.filter(user=request.user, submitted=False)
    if request.method == 'POST':
        cart_items.update(submitted=True)
        return redirect('home-page')
    return render(request, 'myapp/cart_review.html', {'cart_items': cart_items})

def admin_cart_review(request):
    if not request.user.is_staff:
        return redirect('home-page')  # Redirect non-admins to home page

    carts = Cart.objects.filter(submitted=True)
    return render(request, 'myapp/admin_cart_review.html', {'carts': carts})

def update_cart(request):
    if request.method == 'POST':
        if 'update_cart' in request.POST:
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    parts = key.split('_')
                    if len(parts) > 2:
                        cart_id = parts[2]
                        try:
                            cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
                            cart_item.quantity = min(int(value), cart_item.product.quantity)
                            cart_item.save()
                        except ValueError:
                            continue
        elif 'delete_item' in request.POST:
            cart_id = request.POST['delete_item']
            cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
            cart_item.delete()
        elif 'submit_cart' in request.POST:
            for item in Cart.objects.filter(user=request.user, submitted=False):
                if item.quantity > item.product.quantity:
                    # Handle error: not enough stock
                    return redirect('cart-review-with-error')  # Create a URL and view to handle this scenario
                item.submitted = True
                item.status = 'Waiting'
                item.save()
            return redirect('cart-review')
    return redirect('cart-review')

def update_cart_status(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    if request.method == 'POST':
        cart.status = request.POST.get('status')
        cart.save()
        return redirect('admin-cart-review')
    return render(request, 'myapp/update_cart_status.html', {'cart': cart})
