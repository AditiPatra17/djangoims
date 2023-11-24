from django.db import models
from django.contrib.auth.models import User


class Inventory(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    cost_per_item=models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity_in_stock=models.IntegerField(null=False, blank=False)
    quantity_sold=models.IntegerField(null=False, blank=False)
    sales=models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    stock_date=models.DateField(auto_now_add=True)
    last_sales=models.DateField(auto_now=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    def __str__(self) -> str:
        return self.name

