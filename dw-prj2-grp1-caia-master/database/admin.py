from django.contrib import admin
from .models import Customer, Item, Comment, Blog, Entry, CustomerVote

# Register your models here.
admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(Entry)
admin.site.register(CustomerVote)
