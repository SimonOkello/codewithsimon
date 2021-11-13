from django.contrib import admin

# Register your models here.
from .models import  Category,Post, Comment

admin.site.register((Post, Comment))
admin.site.register((Category))