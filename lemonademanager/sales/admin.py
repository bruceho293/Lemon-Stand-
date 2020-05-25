from django.contrib import admin

# Register your models here.
from .models import Sale, Staff, LemonadeProduct, Commission

class CommissionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Sale Comission (%)"   , {'fields': ['sale_commission', 'staff']}),
        ("Confirmation Date"    , {'fields': ['date_applied']}),
    ]
    list_display = ('staff', 'sale_commission', 'date_applied',)

class SaleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Staff'            , {'fields': ['staff_id']}),
        ('Sale Information' , {'fields': ['product_id', 'quantity']}),
    ]
    list_display = ['staff_id', 'product_id', 'quantity']

class StaffAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Staff Information', {'fields': ['name', 'position']})
    ]
    list_display = ['name', 'position']

class LemonadeProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Product Information', {'fields': ['name', 'price']})
    ]
    list_display = ['name', 'price']

admin.site.register(Staff, StaffAdmin)
admin.site.register(LemonadeProduct, LemonadeProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Commission, CommissionAdmin)
