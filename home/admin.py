from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Hotels)
admin.site.register(Emenities)

admin.site.register(Pincode)