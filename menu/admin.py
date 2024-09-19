from django.contrib import admin
from .models import QUANAN, DOAN, DONHANGDICHUYEN, GIOHANG

# Register your models here.
admin.site.register(QUANAN)
admin.site.register(DOAN)
admin.site.register(DONHANGDICHUYEN)
admin.site.register(GIOHANG)