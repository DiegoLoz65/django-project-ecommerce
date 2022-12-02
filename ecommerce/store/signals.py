from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer, Copy, Book

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user = instance)
    
@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    user = instance
    instance.customer.save()

@receiver(post_delete, sender=Copy)
def update_book(sender, instance, **kwargs):
    id = instance.id_book_copy.id_book
    book = Book.objects.get(id_book = id)
    book.total_quantity = (book.total_quantity-1)
    book.save()
