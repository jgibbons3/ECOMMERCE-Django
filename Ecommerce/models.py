from django.db import models

class Clientes(models.Model):
    name = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    phone = models.IntegerField()
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    def has_invoices(self):
        return Invoice.objects.filter(clientes=self.id).count() > 0
    
    def __str__(self):
        return self.name

class Productos(models.Model):
    brand = models.CharField(max_length=30)
    nameproduct = models.CharField(max_length=30)
    description = models.CharField(max_length=70)
    category = models.CharField(max_length=30)
    price = models.FloatField()
    photo = models.ImageField(upload_to='uploads/')
    stock = models.IntegerField()
    
    def __str__(self):
        return self.nameproduct

    def has_invoices(self):
        return Invoice.objects.filter(productos=self.id).count() > 0

class Invoice(models.Model):
    clientes = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Productos, through= 'InvoiceItems')
    number = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    total = models.FloatField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        self.total=self.totalAmount()
        super().save(*args, **kwargs) 

    def totalAmount(self):
        total = 0
        print(total)
        for ii in InvoiceItems.objects.filter(invoice=self.number):
            total += ii.productos.price * ii.totalItem
        return total

    def invoiceItems(self):
        return InvoiceItems.objects.filter(invoice=self.number)

class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    productos = models.ForeignKey(Productos, on_delete=models.CASCADE)
    totalItem = models.IntegerField()
    finalPrice = models.FloatField()

    


