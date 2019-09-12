from django.contrib import admin
from .models import User, Template, Madlib

# Register your models here.

admin.site.register(User)
admin.site.register(Template)
admin.site.register(Madlib)