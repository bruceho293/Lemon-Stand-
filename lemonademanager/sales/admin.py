from django.contrib import admin

# Register your models here.
from .models import Sale, Staff, LemonadeProduct, Commission

admin.site.register(Staff)
admin.site.register(LemonadeProduct)
admin.site.register(Sale)
admin.site.register(Commission)
