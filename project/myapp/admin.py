from django.contrib import admin
from .models import customer, extended, book

admin.site.register(customer)
admin.site.register(extended)
admin.site.register(book)

