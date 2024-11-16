from django.contrib import admin
from store.models import Category,Product,Cart,CartItem,Order,OrderItem,Profile



admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Cart)

admin.site.register(CartItem)


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)