from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    # Products page that displays products within a specific category
    path('category/<int:category_id>/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('process_order/', views.process_order, name='process_order'),
    path('order_success/', views.order_success, name='order_success'), 
    path('my-orders/', views.user_orders, name='user_orders'),
]

