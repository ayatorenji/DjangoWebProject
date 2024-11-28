from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    instock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class contactList(models.Model):
    topic = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    detail = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.topic
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField (max_length=100, default='member')
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    submitted = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default='Waiting', choices=(
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied')
    ))

    def __str__(self):
        return f"{self.quantity} of {self.product.title} - {self.status}"