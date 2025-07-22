from django.db import models
from datetime import timedelta
import random
# Create your models here.

# customer name id number ph number 
#book name id price customer id booked date

class Customer(models.Model):
    name = models.CharField(max_length=100)
    id_number = models.IntegerField(unique =True)
    phone_number = models.CharField(max_length=10)
    address = models.TextField(default="addrs")

    def __str__(self):
        return self.name + " " + str(self.id_number)

class Books_ordered(models.Model):
    name = models.CharField(max_length=100)
    book_id = models.IntegerField()
    customer = models.ForeignKey(
        Customer,
        to_field="id_number",
        on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.delivered_at:
            super().save(*args, **kwargs)
            self.delivered_at = self.created_at + timedelta(days=random.randint(5, 10))
            return super().save(update_fields=['delivered_at'])

        return super().save(*args, **kwargs)


class Books_available(models.Model):
    name = models.CharField(max_length=100)
    book_id = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='books_avalible/', null=True, blank=True)
    stock = models.IntegerField(default=1)