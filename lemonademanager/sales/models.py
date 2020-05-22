from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Staff(models.Model):
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=10)

    # Get the current (latest) commission the staff has at the moment
    @property
    def current_commission(self):
        return Commission.objects.filter(pk=self.pk).order_by('-date_applied').latest().sale_commission

    def __str__(self):
        return "{} (ID: {})".format(self.name, self.id)

class LemonadeProduct(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    @property
    def get_price(self):
        return self.price

    def __str__(self):
        return "{}".format(self.name)

class Commission(models.Model):
    sale_commission = models.DecimalField(max_digits=4, decimal_places=2)
    date_applied = models.DateTimeField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return "{} with commission {}".format(self.staff, self.sale_commission)

class Sale(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    product_id = models.ForeignKey(LemonadeProduct, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    date_sale = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} with Product {}".format(self.staff_id, self.product_id)

    # Get the total price (profit) of this Sale
    @property
    def get_price(self):
        return "%.2f" % (self.product_id.price * self.quantity)

    # Get the commission of the staff from this sale based on the corresponding commission and the date of the sale.
    @property
    def get_staff_commission(self):
        commission = Commission.objects.filter(staff=self.staff_id, date_applied__lte=self.date_sale).latest('date_applied')
        return "%.2f" % (self.product_id.price * self.quantity * (commission.sale_commission / 100))
