from django.db import models
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_count = models.IntegerField(null=True,blank=True)

    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0


    def __str__(self):
        return self.title

CHOICES = (
    (i,i) for  i in range(1,6)
)

class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(choices=CHOICES,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')

    def __str__(self):
        return self.text


