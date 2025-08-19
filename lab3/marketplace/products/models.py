from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image")
    instock = models.PositiveIntegerField(default=0, verbose_name="Items in Stock")
    code = models.CharField(max_length=50, unique=True, verbose_name="Product Code")
    description = models.TextField(verbose_name="Description")
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name='products', verbose_name="Category")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
