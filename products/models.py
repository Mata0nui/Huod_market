from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField((""))
    name_ru = models.CharField("Name in Russian", max_length=100)
    name_ua = models.CharField("Name in Ukrainian", max_length=100)
    name_en = models.CharField("Name in English", max_length=100)
    
# class Color:
#     name = models.CharField(50)
#     hex_color = models.CharField(7 , default="#00000")

    def __str__(self):
        return self.name_ru

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("Title")
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    short_description = models.TextField()
    long_description = models.TextField()
    # palitre = models.ManyToManyField(Color, blank=True, related_name="products")
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
