from django.contrib import admin
from .models import Customer, Books_available, Books_ordered


# Register your models here.
admin.site.register(Customer)
admin.site.register(Books_ordered)
admin.site.register(Books_available)
