from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import *
from django.forms import ModelForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Count

#Menu
def totalClientes(request):
    cliente_total=Clientes.objects.all()
    total_earning=Invoice.objects.all().aggregate(Sum('total')).get('total__sum', 0.00)
    total_invoices=Invoice.objects.all()
    total_products=Productos.objects.all()
    dataset=Invoice.objects.extra(select={'day': 'date'}).values('day') \
               .annotate(available=Sum('total'))
    lowStock=Productos.objects.extra(select={'products': 'nameproduct'}).values('products')\
                .annotate(available=Sum('stock')).order_by('available')[:5]
    return render(request, 'Ecommerce/menu.html', {
        'cliente_total': cliente_total,
        'total_earning': total_earning,
        'total_invoices': total_invoices,
        'total_products': total_products,
        'dataset': dataset,
        'lowStock': lowStock
    })

def TopFiveProducts(request):
    topFive=Productos.objects.extra(select={'a': 'nameproduct'}).values('a')\
        .annotate(available=Sum('invoiceitems__totalItem')).order_by('-available')[:5]
    return render(request, 'Ecommerce/topFiveProducts.html', {
        'topFive': topFive
    })


def TopFiveClients(request):
    topFiveClients=Clientes.objects.extra(select={'a': 'name'}).values('a')\
        .annotate(available=Sum('invoice__total')).order_by('-available')[:5]
    return render(request, 'Ecommerce/topFiveClient.html', {
        'topFiveClients': topFiveClients
    })


#Client List
def ClientesList(request):
    cliente_list=Clientes.objects.all()
    return render(request, 'Ecommerce/listaClientes.html', {'cliente_list': cliente_list})


class PostsClientes(ModelForm):
    class Meta:
        modelClientes = Clientes
        fieldsClientes = ['name', 'apellido', 'phone', 'email', 'address']

#Invoices per client
def ClientInvoices(request, id):
    invoice_list=Invoice.objects.filter(clientes=id)
    return render(request, 'Ecommerce/listaInvoice.html', {'invoice_list': invoice_list})

#Productos
def ProductosList(request):
    productos_list=Productos.objects.all()
    return render(request, 'Ecommerce/listaProductos.html', {'productos_list': productos_list})

class PostsProducts(ModelForm):
    class Meta:
        model = Productos
        fields = ['brand', 'nameproduct', 'description', 'category', 'price', 'photo', 'stock']

def ProductDelete(request, id):
    print (id)
    post = get_object_or_404(Productos, id=id)
    post.delete()
    #messages.add_message(request, messages.SUCCESS, 'Product successfully deleted.')
    return redirect ('viewProducts')

    
def ProductUpdate(request, id): 
    product = get_object_or_404(Productos, id=id)
    form = PostsProducts(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect ('viewProducts')
    return render(request, 'Ecommerce/ProductForm.html', {'form': form})


def ProductCreate(request):
    form = PostsProducts(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect ('viewProducts')
    return render(request, 'Ecommerce/newProduct.html', {'form': form})


def ProductInvoices(request, id):
    invoice_list=Invoice.objects.filter(productos=id)
    return render(request, 'Ecommerce/listaInvoice.html', {'invoice_list': invoice_list})


#Invoice
def InvoiceList(request):
    invoice_list=Invoice.objects.all()
    return render(request, 'Ecommerce/listaInvoice.html', 
    {'invoice_list': invoice_list}
    )

class PostsInvoice(ModelForm):
    class Meta:
        modelInvoice = Invoice
        fieldsInvoice = ['clientes', 'productos', 'number', 'date', 'total']







