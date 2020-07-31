from django.db import models
import jsonfield


class Book(models.Model):
    #id = models.AutoField(primary_key=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False)
    code = models.TextField()
    book_type = models.CharField(max_length=100, blank=False)
    daily_rental_charge = jsonfield.JSONField(blank=False, default={})

    class Meta:
        ordering = ['title']
        unique_together = ("title", "code")



class Rental(models.Model):
    #id = models.AutoField(primary_key=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=100, blank=False)
    total_rental_charge = models.DecimalField(decimal_places=4,max_digits=25,blank=False)
    books_data = jsonfield.JSONField(blank=False, default={})

