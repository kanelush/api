from django.contrib import admin
from .models import Category, Negocios, Contact, Competencia, Producto, Token, PurchaseData, Cart
# Register your models here.
admin.site.register(Category)
admin.site.register(Negocios)
admin.site.register(Contact)
admin.site.register(Competencia)
admin.site.register(Producto)
admin.site.register(Token)
admin.site.register(PurchaseData)
admin.site.register(Cart)
