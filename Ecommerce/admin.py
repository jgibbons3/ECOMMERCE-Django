from django.contrib import admin

from .models import Clientes 
from .models import Productos
from .models import Invoice, InvoiceItems

class InvoiceItemAdmin(admin.TabularInline):
    model=Invoice.productos.through
    extra = 3

class InvoiceAdmin(admin.ModelAdmin):
    inlines=(InvoiceItemAdmin,)

admin.site.register(Clientes)
admin.site.register(Productos)
admin.site.register(Invoice, InvoiceAdmin) 
admin.site.register(InvoiceItems) 


