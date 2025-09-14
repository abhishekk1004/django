from django.db import models



class Product(models.Model):

    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)

    sku = models.CharField(max_length=64, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} — {self.name}"

