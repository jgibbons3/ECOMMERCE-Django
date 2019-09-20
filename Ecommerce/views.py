from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import *
from django.forms import ModelForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

from .form import UserCreationForm

#Sale user view
@login_required
def Sale(request):
    productos_list=Productos.objects.all()
    return render(request, 'Ecommerce/sale.html', {'productos_list': productos_list})

#Login
def my_view(request):
    if request.user.is_staff:
        return redirect('/')
    else:
        return redirect('Sale/')


#Signup
def Signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accounts/login/')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'Ecommerce/signup.html', {'form': form})


#Menu
@login_required
def totalClientes(request):
    cliente_total=Clientes.objects.filter(is_staff=False)
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

@login_required
def TopFiveProducts(request):
    topFive=Productos.objects.extra(select={'a': 'nameproduct'}).values('a')\
        .annotate(available=Sum('invoiceitems__totalItem')).order_by('-available')[:5]
    return render(request, 'Ecommerce/topFiveProducts.html', {
        'topFive': topFive
    })

@login_required
def TopFiveClients(request):
    topFiveClients=Clientes.objects.extra(select={'a': 'name'}).values('a')\
        .annotate(available=Sum('invoice__total')).order_by('-available')[:5]
    return render(request, 'Ecommerce/topFiveClient.html', {
        'topFiveClients': topFiveClients
    })


#Client List
@login_required
def ClientesList(request):
    cliente_list=Clientes.objects.filter(is_staff=False)
    return render(request, 'Ecommerce/listaClientes.html', {'cliente_list': cliente_list})


class PostsClientes(ModelForm):
    class Meta:
        modelClientes = Clientes
        fieldsClientes = ['user', 'first_name', 'last_name', 'phone', 'email', 'address']

#Invoices per client
@login_required
def ClientInvoices(request, id):
    invoice_list=Invoice.objects.filter(clientes=id)
    return render(request, 'Ecommerce/listaInvoice.html', {'invoice_list': invoice_list})

#Productos
@login_required
def ProductosList(request):
    productos_list=Productos.objects.all()
    return render(request, 'Ecommerce/listaProductos.html', {'productos_list': productos_list})

class PostsProducts(ModelForm):
    class Meta:
        model = Productos
        fields = ['brand', 'nameproduct', 'description', 'category', 'price', 'photo', 'stock']

@login_required
def ProductDelete(request, id):
    print (id)
    post = get_object_or_404(Productos, id=id)
    post.delete()
    #messages.add_message(request, messages.SUCCESS, 'Product successfully deleted.')
    return redirect ('viewProducts')

@login_required    
def ProductUpdate(request, id): 
    product = get_object_or_404(Productos, id=id)
    form = PostsProducts(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect ('viewProducts')
    return render(request, 'Ecommerce/ProductForm.html', {'form': form})

@login_required
def ProductCreate(request):
    form = PostsProducts(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect ('viewProducts')
    return render(request, 'Ecommerce/newProduct.html', {'form': form})

@login_required
def ProductInvoices(request, id):
    invoice_list=Invoice.objects.filter(productos=id)
    return render(request, 'Ecommerce/listaInvoice.html', {'invoice_list': invoice_list})


#Invoice
@login_required
def InvoiceList(request):
    invoice_list=Invoice.objects.all()
    return render(request, 'Ecommerce/listaInvoice.html', 
    {'invoice_list': invoice_list}
    )

class PostsInvoice(ModelForm):
    class Meta:
        modelInvoice = Invoice
        fieldsInvoice = ['clientes', 'productos', 'number', 'date', 'total']







