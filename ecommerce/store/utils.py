import json
from .models import *


def cookieCart(request):
	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:	
			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
				cartItems += cart[i]['quantity']

				book = Book.objects.get(id_book=i)
				total = (book.price * cart[i]['quantity'])

				order['get_final_price'] += total
				order['get_final_books'] += cart[i]['quantity']

				item = {
				'id':book.id,
				'product':{'id':book.id_book,'name':book.title, 'price':book.price, 
				'imageURL':book.imageURL}, 'quantity':cart[i]['quantity'],
				'digital':book.digital,'get_total':total,
				}
				items.append(item)

				if book.digital == False:
					order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
		
        #'get_or_create' permite buscar por parametro y si no existe entonces lo crea y lo guarda en created
        order, new_order = Order.objects.get_or_create(dni_customer1 = customer, complete = False)
        """
        Retorna los objetos del modelo OrderDetails respecto
        al número de orden que tiene el usuario
        """
        details = order.details_set_all
        total_books = order.get_final_books
    
    else:
        cookie_data = cookieCart(request)
        total_books = ''
        order = ''
        details = ''
        
    return {
        'total_books':total_books,
        'order':order,
        'details':details
        }

def bookingData(request):
	if request.user.is_authenticated:
		customer = request.user.customer

		booking = Booking.objects.filter(
			dni_customer2 = customer
		)

		book = booking.values('reserved_book')
		total_books = booking.values('quantity')

	return {
		'book':book,
		'total_books':total_books
	}

def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	books_cookie = cookieData['books']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for cookie in books_cookie:
		book = Book.objects.get(id=book['id'])
		orderDetails = OrderDetails.objects.create(
			book = book,
			ordern= order,
			quantity = (cookie['quantity'] if cookie['quantity']>0 else -1 * cookie['quantity']), # negative quantity = freebies
		)
	return customer, order

