from django.urls import path
from django.urls import include
from . import views 
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404 as handler404

#se agrego un libro 
urlpatterns = [
    path('', views.index, name ='index'),
    path('store/', views.store, name ='store'),
    path('', include('django.contrib.auth.urls')),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name ='cart'),
    path('exit/', views.exit, name = 'exit'),
    path('checkout/', views.checkout, name ='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('update_card/', views.updateCard, name="update_card"),
    path('process_order/', views.processOrder, name="process_order"),
    path('order_history/', views.OrderHistory, name="order_history"),
    path('signin/', views.signin, name ='signin'),
    path('signup/', views.signup, name ='signup'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('bookings/', views.bookings, name='bookings'),
    path('manage_balance/', views.manage_balance, name='manage_balance'),
    path('add_card/', views.add_card, name='add_card'),
    path('news/', views.news, name='news'),
    path('return_order/<str:order_number>', views.return_order, name='return_order'),
    path('shops/', views.shops, name='shops'),
    path('news/', views.news, name='news'),
    path('pickup_store/', views.pickup_store, name='pickup_store'),
    path('item/<str:id_book>/', views.item, name='item'),
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='user/password_reset.html'
            ), 
        name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='user/password_reset_done.html'
            ), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html'
            ), 
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='user/password_reset_complete.html'
            ), 
        name='password_reset_complete'),
]

handler404 = "store.views.custom_page_not_found_view"