from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from store.models import Customer
from .forms import *
from django.db import IntegrityError
from django.db import models
from django.contrib import messages
from .utils import cartData, guestOrder
from .models import *
import json
from django.utils.translation import gettext
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
#from django.shortcuts import render_to_response
from django.shortcuts import render
from .models import Book
from datetime import timedelta
from django.db.models.functions import Now
from django.shortcuts import render
from django.template import RequestContext


def index(request):
    data = cartData(request)
    order = data['order']
    context = {
        'order': order,
    }
    return render(request, 'store/index.html', context)

def store(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(title__icontains = query) |
            Q(author__icontains = query) |
            Q(editorial__icontains = query)
        )
        books = Book.objects.filter(qset, total_quantity__gt = 0).distinct()
        quantity = books.__len__()
    else:
        data = cartData(request)
        total_books = data['total_books']
        details = data['details']
        order = data['order']
        
        books = Book.objects.filter(total_quantity__gt = 0)
        quantity= books.__len__()

    data = cartData(request)
    total_books = data['total_books']
    order = data['order']
    total_books = data['total_books']
    context = {
        'total_books':total_books,
        'books':books,
        'order':order,
        'quantity':quantity,
        }

    return render(request, 'store/store.html', context)

def cart(request):
    det = OrderDetails.objects.filter(quantity__lt = 1).delete()
    data = cartData(request)

    total_books = data['total_books']
    order = data['order']
    details = data['details']
        
    for detail in details:
        id = detail.book_order.id_book
        book = Book.objects.get(id_book = id)
        if detail.quantity > book.total_quantity:
            detail.quantity = book.total_quantity
            detail.save()
    
    # retorna el render de los items al template de cart
    context = {
        'total_books': total_books,
        'details': details,
        'order': order}
    return render(request, 'store/cart.html', context)

@login_required
def bookings(request):
    data = cartData(request)
    order = data['order']

    customer = request.user.customer

    booking = Booking.objects.filter(
			dni_customer2 = customer, complete=False
		)

    total_reserved_books = 0
    total_price = 0
    for i in booking:
        total_reserved_books += i.quantity
        total_price += (i.reserved_book.price*i.quantity)

    context = {
        'total_price': total_price,
        'total_reserved_books': total_reserved_books,
        'booking': booking,
        'order':order,
    }

    if request.GET.get('add_to_order'):
        
        order, new_order = Order.objects.get_or_create(
            dni_customer1=customer, complete=False)
        print(f"ID Orden: {order.order_number}")

        for i in booking:
            print(i.reserved_book)
            print(i.quantity)
            i.complete = True
            i.save()
            details, new_order = OrderDetails.objects.get_or_create(
                book_order=i.reserved_book, order_number=order)
            print(f"ID Detalle: {details.id_details}")

            if details.quantity < 3:
                details.quantity = (details.quantity + i.quantity)
                
            details.save()
        return redirect(to='/checkout/')

    return render(request, 'user/bookings.html', context)

@login_required
def checkout(request):
    customer = request.user.customer
    
    if request.method == 'POST':
        shipping_form = AddressShippingForm(request.POST)
        order, new_order = Order.objects.get_or_create(
            dni_customer1=customer, complete=False)
        details = order.details_set_all
        for i in details:
            book = Book.objects.get(id_book = i.book_order_id)
            book.total_quantity = book.total_quantity - i.quantity 
            book.save()
        final_price = order.get_final_price
        if shipping_form.is_valid() and customer.balance > final_price:
            customer.balance = (customer.balance - final_price)
            shipping = shipping_form.save(commit=False)
            shipping.order_number_shipping_id = order.order_number
            order.complete = True
            order.save()
            shipping.save()
            customer.save()
            return redirect('order_history')
        else:
            messages.error(request,'You do not have insufficient balance, please increase your balance.')
    else:
        shipping_form = AddressShippingForm()
    data = cartData(request)

    total_books = data['total_books']
    order = data['order']
    details = data['details']

    context = {
        'total_books': total_books,
        'order': order,
        'details': details,
        'shipping_form': shipping_form,
        }

    return render(request, 'store/checkout.html', context)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        formUser = UserRegisterForm(request.POST)
        formCustomer = CustomerRegisterForm(request.POST)
        if formUser.is_valid() and formCustomer.is_valid():
            user = formUser.save()
            customer = formCustomer.save(commit=False)
            customer.user = user
            customer.save()
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username entered is invalid')
    else:
        formUser = UserRegisterForm()
        formCustomer = CustomerRegisterForm()
    return render(request, 'autentication/signup.html', {'formUser': formUser, 'formCustomer': formCustomer})

def exit(request):
    logout(request)
    return redirect(to='/')

def signin(request):
    if request.method == 'GET':
        return render(request, 'autentication/signin.html', {
            'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'autentication/signin.html', {
                'form': AuthenticationForm,
                'error': 'Username and password did not match',
            })
        else:
            login(request, user)
            return redirect(to='/')

def error(request):
    data = cartData(request)
    order = data['order']

    context = {
        'order':order,
    }
    return render(request, 'autentication/error.html', context)

# Necesary to update the customer info
@login_required
def profile(request):
    return render(request, 'user/update_profile.html')

@login_required
def update_profile(request):
    data = cartData(request)
    order = data['order']

    if request.method == 'POST':
        p_form = CustomerUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.customer)
        if p_form.is_valid():
            p_form.save()
            return redirect(to='/')

    else:
        p_form = CustomerUpdateForm(instance=request.user.customer)

    context = {
        'p_form': p_form,
        'order': order,
    }

    return render(request, 'user/update_profile.html', context)

def search(request):
    query = request.GET.get('q', '')
    print(query)
    if query:
        qset = (
            Q(title__icontains = query) |
            Q(author__icontains = query) )
        books = Book.objects.filter(qset).distinct()
    else:
        books = []

    context = {
        'books':books}
    return render(request, 'store/store.html', context)

def updateItem(request):

    data = json.loads(request.body)

    # __SE CREAN INSTANCIAS DE LOS DATOS PASADOS POR json__#
    id_book = data['productId']
    action = data['action']
    print('Action:', action)
    print('Book:', id_book)

    # __INFORMACIÓN DEL CUSTOMER PASADA POR PARAMETRO__#
    customer = request.user.customer

    if action == 'add':
        #__GUARDA EL OBJETO DEL MODELO Book CON LLAVE PRIMARIA IGUAL A LA DE 'productId'__#
        book = Book.objects.get(id_book = id_book)
        print(f"Titulo: {book.title}")

        # __GUARDA EL OBJETO DEL MEDELO Order CON LLAVE FORNEA IGUAL A LA DEL Customer__#
        order, new_order = Order.objects.get_or_create(
            dni_customer1=customer, complete=False)
        print(f"ID Orden: {order.order_number}")

        # __GUARDA EL OBJETO DE OderDetails CON book Y order__#
        details, new_order = OrderDetails.objects.get_or_create(
            book_order=book, order_number=order)
        print(f"ID Detalle: {details.id_details}")

        details_quantity = OrderDetails.objects.filter(order_number = order)
        print("LA CANTIDAD ES:", details_quantity.__len__())

        if details.quantity == 3:
            print("Error...")
            messages.error(request,'username or password not correct')
        
        #__DEPENDIENDO DE LA ACCIÓN SE AGREGA O REMUEVE UN LIBRO DE 'quantity'__#
        if details.quantity < 3 and book.total_quantity > 0 and (book.total_quantity>details.quantity) and (details_quantity.__len__() <= 5):
            details.quantity = (details.quantity + 1)
            print("Agregado con exito...")
        
        # __GUARDAR CAMBIOS__#
        details.save()

    elif action == 'remove':
        #__GUARDA EL OBJETO DEL MODELO Book CON LLAVE PRIMARIA IGUAL A LA DE 'productId'__#
        book = Book.objects.get(id_book = id_book)
        print(f"Titulo: {book.title}")

        # __GUARDA EL OBJETO DEL MEDELO Order CON LLAVE FORNEA IGUAL A LA DEL Customer__#
        order, new_order = Order.objects.get_or_create(
            dni_customer1=customer, complete=False)
        print(f"ID Orden: {order.order_number}")

        # __GUARDA EL OBJETO DE OderDetails CON book Y order__#
        details, new_order = OrderDetails.objects.get_or_create(
            book_order=book, order_number=order)
        print(f"ID Detalle: {details.id_details}")

        details.quantity = (details.quantity - 1)
        # __GUARDAR CAMBIOS__#
        details.save()

        #__BORRA EL LIBRO CUANDO ES IGUAL 0__#
        if details.quantity <= 0 :
            details.delete()

    elif action == 'reserve':
        #__GUARDA EL OBJETO DEL MODELO Book CON LLAVE PRIMARIA IGUAL A LA DE 'productId'__#
        book = Book.objects.get(id_book = id_book)
        print(f"Titulo: {book.title}")

        booking_quantity = Booking.objects.filter(dni_customer2=customer, complete=False)

        if book.total_quantity > 0 and booking_quantity.__len__() < 5:
            booking, new_booking = Booking.objects.get_or_create(
                dni_customer2=customer,
                reserved_book=book, complete = False)
            print(f"ID Booking: {booking.id_booking}")


            if booking.quantity < 3:
                booking.quantity = (booking.quantity + 1)
                book.total_quantity = (book.total_quantity - 1)
                book.save()
                print(booking.quantity)
                print("Reservado con exito...")
                booking.save()

    elif action == 'remove_reserve':
        #__GUARDA EL OBJETO DEL MODELO Book CON LLAVE PRIMARIA IGUAL A LA DE 'productId'__#
        book = Book.objects.get(id_book = id_book)
        print(f"Titulo: {book.title}")

        booking, new_booking = Booking.objects.get_or_create(
            dni_customer2=customer,
            reserved_book=book,
            complete=False)
        print(f"ID Booking: {booking.id_booking}")

        booking.quantity = (booking.quantity - 1)
        book.total_quantity = (book.total_quantity + 1)
        book.save()
        booking.save()

        if booking.quantity <= 0:
            booking.delete()
    return JsonResponse('Book was added. ', safe=False)

def processOrder(request):
    #transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, new_order = Order.objects.get_or_create(
            dni_customer1=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    #order.transaction_id = transaction_id

    # __ORDEN DECLARADA COMO COMPLETA__#
    if total == order.get_final_price:
        order.complete = True
    order.save()

    # __SI EL LIBRO NO ES DIGITAL ENTONCES SE CREA UNA ORDEN DE ENVIO__#
    if order.shipping == True:
        pass

    return JsonResponse('Payment submitted..', safe=False)

@login_required
def manage_balance(request):
    data = cartData(request)
    order = data['order']
    pk = request.user.id
    customer = request.user.customer
    balance = request.user.customer.balance
    payment_methods = PaymentMethod.objects.filter(customer=pk)
    context = {
        'balance': balance,
        'payment_methods': payment_methods,
        'order':order,
    }

    if request.GET.get('add') and (customer.balance + 50000 <= 500000) and (payment_methods.__len__()>0):
        customer.balance = customer.balance + 50000
        customer.save()
        return redirect(to='/manage_balance/')
    if request.GET.get('subtract') and (payment_methods.__len__()>0):
        customer.balance = customer.balance - 50000
        if customer.balance < 0:
            customer.balance = 0
        customer.save()
        return redirect(to='/manage_balance/')
    else:
        return render(request, 'user/manage_balance.html', context)

@login_required
def updateCard(request):
    data = json.loads(request.body)

    card_id = data['cardId']
    action_card = data['action']
    
    if action_card == 'delete':
        PaymentMethod.objects.filter(id = card_id).delete()

    return JsonResponse('Card was delete. ', safe=False)

@login_required
def add_card(request):
    data = cartData(request)
    order = data['order']
    if request.method == 'POST':
        customer = request.user.customer
        formCard = AddCardForm(request.POST, instance=customer)
        if formCard.is_valid():
            type_card = formCard.data['type_card']
            number_card = formCard.data['number_card']
            cvv = formCard.data['cvv']
            cardholder = formCard.data['cardholder']
            expiration_date = formCard.data['expiration_date']
            paymentmethod = PaymentMethod.objects.create(customer=customer,
                                                         type_card=type_card,
                                                         number_card=number_card,
                                                         cvv=cvv,
                                                         cardholder=cardholder,
                                                         expiration_date=expiration_date
                                                         )
            paymentmethod.save()
            return redirect(to='/manage_balance/')
        else:
            messages.info(request, 'Data invalid.')
    else:
        formCard = AddCardForm()
    return render(request, 'user/add_card.html', {'formCard': formCard, 'order':order})

def item(request, id_book):
    data = cartData(request)
    order = data['order']
    book = Book.objects.filter(id_book=id_book)
    f_books = Book.objects.filter(total_quantity__gt = 0)
    books = []
    i=0
    while i < 4:
        books.append(f_books[i])
        i+=1
        
    return render(request, 'store/item.html', {'book': book, 'order':order, 'books':books})

def shops(request):
    data = cartData(request)
    order = data['order']
    offices = BranchOffice.objects.all()
    print(offices)
    context = {
        'offices':offices,
        'order':order,
    }
    return render(request, 'store/shops.html', context)

def OrderHistory(request):
    data = cartData(request)
    order = data['order']
    customer = request.user.customer
    
    shippings_history = []
    pickups_history = []
    order_history = []
    
    orderHistory = Order.objects.filter(
        dni_customer1=customer, complete=True)
    for i in orderHistory:
        try:
            shippings = Shipping.objects.get(
                order_number_shipping = i
            )
        except Shipping.DoesNotExist:
            break
        shippings_history.append(shippings)
        orderDetailsHistory = OrderDetails.objects.filter(
            order_number = i
        )
        order_history.append(orderDetailsHistory)
    
    bookings = Booking.objects.filter(
			dni_customer2 = customer, complete=True
		)

    mylist = zip(order_history, orderHistory, shippings_history)
    context = {
        'order':order,
        'mylist': mylist,
        'bookings':bookings,
    }
    return render(request, 'user/order_history.html', context)

def about(request):
    data = cartData(request)
    order = data['order']

    context = {
        'order':order,
    }
    return render(request, 'store/about.html', context)

def return_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    details = order.details_set_all
    customer = request.user.customer
    if request.method == 'POST':
        form = ReturnOrderForm(request.POST)
        if form.is_valid():
            shipping = Shipping.objects.get(order_number_shipping=order_number)
            shipping.state_shipping = STATE_SHIPPING_CHOICES[3][0]
            shipping.save()

            customer.balance = customer.balance + order.get_final_price
            customer.save()

            for i in details:
                book = Book.objects.get(id_book = i.book_order_id)
                book.total_quantity = book.total_quantity + i.quantity 
                book.save()

            return redirect(to='/order_history/')

    else:
        form = ReturnOrderForm()

    context = {
        'order':order,
        'form':form
    }
    return render(request, 'user/return_order.html', context)

def news(request):
    data = cartData(request)
    order = data['order']

    context = {
        'order':order,
    }
    return render(request, 'store/news.html', context)

def pickup_store(request):
    data = cartData(request)
    total_books = data['total_books']
    order = data['order']
    details = data['details']
    branchOffices = []
    branchOffices = BranchOffice.objects.all()
    customer = request.user.customer

    if request.POST:
        branch = request.POST['branch']
        order, new_order = Order.objects.get_or_create(
            dni_customer1=customer, complete=False)

        details = order.details_set_all

        for i in details:
            book = Book.objects.get(id_book = i.book_order_id)
            book.total_quantity = book.total_quantity - i.quantity 
            book.save()

        final_price = order.get_final_price

        if customer.balance > final_price:
            customer.balance = (customer.balance - final_price)
            pickup = PickUpStore.objects.create(order_number_pickup = order)
            pickup.order_number_pickup = order
            pickup.state_shipping = STATE_PICKUP_CHOICES[0][0]
            select_store = BranchOffice.objects.get(pk=branch).name
            pickup.branch_office_pickup = select_store
            print(pickup)
            pickup.save()

            order.complete = True
            order.save()
            customer.save()
            return redirect('order_history')
        else:
            messages.error(request,'You do not have insufficient balance, please increase your balance.')


    context = {
        'total_books': total_books,
        'order': order,
        'details': details,
        'branchOffices': branchOffices
        }

    return render(request, 'store/pickup.html', context)

def custom_page_not_found_view(request, exception):
    return render(request, "autentication/error.html", {})