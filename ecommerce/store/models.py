from email.policy import default
from secrets import choice
from sqlite3 import complete_statement
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cities_light.models import Country, Region, City
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import RegexValidator
from datetime import time, date, datetime, timezone
from datetime import timedelta
from django.db import models
from django.utils.timezone import now

# Create your models here.
GENDER_CHOICES =(
    ("Universal literature", "Universal literature"),
    ("General", "General"),
    ("Terror and suspense", "Terror and suspense"),
    ("Historical", "Historical"),
    ("Romance", "Romance"),
    ("Science fiction and Fantasy", "Science fiction and Fantasy"),
)

DAY_CHOICES =(
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
)

CAUSE_RETURN_CHOICES = (
    ("Product in poor shape", "Product in poor shape"),
    ("It did not meet my expectations", "It did not meet my expectations"),
    ("The order arrived in a time superior to the stipulated", "The order arrived in a time superior to the stipulated"),
)

STATE_SHIPPING_CHOICES = (
    ("PREPARING", "PREPARING"),
    ("SENT", "SENT"),
    ("DELIVERED", "DELIVERED"),
    ("CANCELED FOR RETURN", "CANCELED FOR RETURN"),
)

STATE_PICKUP_CHOICES = (
    ("IN SHOP", "IN SHOP"),
    ("PICKED UP", "PICKED UP"),
)

GENDER_PERSON_CHOICES =(
    ("Male", "Male"),
    ("Female", "Female"),
)

TYPE_CARD =(
    ("Debit card", "Debit card"),
    ("Credit card", "Credit card"),
)

STATE_COPY =(
    ("D", "Disponible"),
    ("V", "Vendido"),
    ("R", "Reservado"),
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer')
    dni = models.IntegerField(blank=False, null=True)
    name_regex = RegexValidator(regex=r'[a-zA-Z_.-]+$' , message="Please enter a valid name")
    name = models.CharField(validators=[name_regex], max_length=200, blank=False)
    surname_regex = RegexValidator(regex=r'[a-zA-Z_.-]+$' , message="Please enter a valid surname")
    surname = models.CharField(validators=[surname_regex], max_length=200, blank=False)
    date_birth = models.DateField(blank=False, null=True)
    gender = models.CharField(max_length=200, choices=GENDER_PERSON_CHOICES, default = 'Male', null=True)
    email = models.EmailField(max_length = 200, blank=False, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Please enter a valid phone number.")
    cellphone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    literary_prefer = models.CharField(max_length=200, blank=True, choices=GENDER_CHOICES, default = '1')
    balance = models.IntegerField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,  blank=True, null=True)
    region = ChainedForeignKey(Region, chained_field="country", chained_model_field="country",  blank=True, null=True)
    city = ChainedForeignKey(City, chained_field="region", chained_model_field="region",  blank=True, null=True)

    def __str__(self):
        return self.name
        
class PaymentMethod(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type_card = models.CharField(max_length=200, choices=TYPE_CARD)
    number_card = models.IntegerField(blank=False)
    cvv = models.IntegerField(blank=False, validators=[MaxValueValidator(999)])
    cardholder_regex = RegexValidator(regex=r'[a-zA-Z_.-]+$' , message="Please enter a valid name for the cardholder.")
    cardholder = models.CharField(validators=[cardholder_regex], max_length=200, blank=False)
    expiration_date = models.DateField(null=True)

class Order(models.Model):
    order_number = models.BigAutoField(primary_key=True)
    dni_customer1 = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    final_price = models.IntegerField(default = 0)  
    complete = models.BooleanField(default = False)

    @property
    def get_final_price(self):
        total = 0
        orderdetails = self.orderdetails_set.all()
        for i in orderdetails:
            total += i.quantity * i.book_order.price
        
        return total
        
    
    @property
    def shipping(self):
        shipping = False
        orderdetails = self.orderdetails_set.all()
        for i in orderdetails:
            if i.book_order.digital == False:
                shipping = True
        return shipping

    @property
    def get_final_books(self):
        orderdetails = self.orderdetails_set.all()
        total_libros = sum([detail.quantity for detail in orderdetails])
        return total_libros

    @property
    def details_set_all(self):
        orderdetails = self.orderdetails_set.all()
        return orderdetails
    
class Book(models.Model):
    id_book = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.CharField(max_length=200, blank=False, null=False)
    literary_gender = models.CharField(max_length=200, choices=GENDER_CHOICES)
    number_pages = models.IntegerField(null=False, blank=False)
    editorial = models.CharField(max_length=200, blank=False, null=False)
    issn = models.IntegerField(null=False, blank=False)
    idiom = models.CharField(max_length=200, blank=False, null=False)
    publication_date = models.DateTimeField(auto_now=False)
    price = models.IntegerField(null=False, blank=False)
    image = models.ImageField(null= True, blank=True)
    digital = models.BooleanField(default = False)
    total_quantity = models.IntegerField(default=0)
    """
    La funcion imageURL accede a los atriburos de los campos mediante el
    decorador @property si el atributo guarda un valor entonces lo 
    retorna y si ocurre algun error retorna un string vacio -
    """
    @property
    def imageURL(self): 
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return "{}  [{}]".format(self.title,self.issn)

class OrderDetails(models.Model):
    id_details = models.BigAutoField(primary_key=True)
    book_order = models.ForeignKey(Book, on_delete=models.CASCADE) 
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=False, blank=False)
    added_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id_details)
        
    def subtotal_price(self):
            return int(self.quantity * self.book_order.price)

    def book(self):
        return self.book_order
    
    def order(self):
        return self.order_number
    
    def get_quantity(self):
        return self.quantity

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin')
    dni_admin = models.IntegerField(blank=False, null=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    surname = models.CharField(max_length=200, null= False, blank=False)
    date_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=200, choices=GENDER_PERSON_CHOICES)
    email = models.EmailField(max_length = 200, null= False, blank=False)
    cellphone_number = models.IntegerField(null = False, blank=False)

    def complete_name(self):
        return "{} {}".format(self.name, self.surname)

    def __str__(self):
        return self.complete_name()

class Schedule(models.Model):
    id_schedule = models.BigAutoField(primary_key=True)
    day = models.CharField(max_length=200, choices = DAY_CHOICES)
    opening_hour = models.TimeField(auto_now=False, auto_now_add=False)
    closing_hour = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.day

class BranchOffice(models.Model):
    id_branch_office = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    #Is necesary change the field to list of the cities and departments in Colombia
    department = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200)
    phone = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

class Quantity(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=True)
    quantity = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return str(self.quantity) 
    
    def clean(self):
        copy = Copy
        id_book_copy = self.book
        id_branch_office = self.branch_office
        is_used = self.is_used
        quantity = Book.objects.get(id_book = self.book.id_book)
        total_quantity = quantity.total_quantity + self.quantity
        book = Book.objects.filter(id_book = self.book.id_book).update(total_quantity = total_quantity)
        for i in range(self.quantity):
            Copy.objects.create(
                id_book_copy = id_book_copy,
                id_branch_office = id_branch_office,
                is_used = is_used,
                state = STATE_COPY[0][0]
                )

class Copy(models.Model):
    id_copy = models.BigAutoField(primary_key=True)
    id_book_copy = models.ForeignKey(Book, on_delete = models.CASCADE)
    id_branch_office = models.ForeignKey(BranchOffice, on_delete = models.CASCADE)
    is_used = models.BooleanField(null=True)
    state = models.CharField(max_length=10, choices=STATE_COPY, blank=False,  null=False)
    #id_quantity = models.ForeignKey(Quantity, on_delete = models.CASCADE, null=True)

    def complete_name(self):
        return "{}, {}".format(self.id_book_copy, self.id_copy)

    def __str__(self):
        return self.complete_name()

    def clean(self):
        print('HOLA')
        
class Booking(models.Model):
    id_booking = models.BigAutoField(primary_key=True)
    dni_customer2 = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reserved_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    booking_hour = models.DateTimeField(auto_now_add=True, db_index=True)
    complete = models.BooleanField(default = False)

    def __str__(self):
        return "Reserva #{}  [Cliente: {}]".format(self.id_booking, self.dni_customer2)

class ReturnOrder(models.Model):
    id_return_order = models.BigAutoField(primary_key=True)
    order_number_return = models.ForeignKey(Order, on_delete=models.CASCADE)
    cause = models.CharField(max_length=200, choices=CAUSE_RETURN_CHOICES)
    description = models.TextField(max_length=400)

    def __str__(self):
        return str(self.id_return_order)

class Shipping(models.Model):
    id_shipping = models.BigAutoField(primary_key=True)
    order_number_shipping = models.ForeignKey(Order, on_delete=models.CASCADE)
    state_shipping = models.CharField(max_length=200, choices=STATE_SHIPPING_CHOICES, default=STATE_SHIPPING_CHOICES[0][0])
    date_shipping = models.DateField(auto_now=True)
    address_shipping = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,  blank=True, null=True)
    region = ChainedForeignKey(Region, chained_field="country", chained_model_field="country",  blank=True, null=True)
    city = ChainedForeignKey(City, chained_field="region", chained_model_field="region",  blank=True, null=True)
    
    def __str__(self):
        return str(self.id_shipping)

class PickUpStore(models.Model):
    id_pickup_store = models.BigAutoField(primary_key=True)
    order_number_pickup = models.ForeignKey(Order, on_delete=models.CASCADE)
    state_shipping = models.CharField(max_length=200, choices=STATE_PICKUP_CHOICES)
    #Select options saved in the branch_office
    branch_office_pickup = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id_pickup_store) 
