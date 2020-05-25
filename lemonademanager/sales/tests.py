from django.test import TestCase

from sales.models import Staff, LemonadeProduct, Commission, Sale
from django.utils import timezone
import datetime

def create_commission(commission, days, staff):
    time = timezone.now() + datetime.timedelta(days=days)
    return Commission.objects.create(sale_commission=commission, date_applied=time, staff=staff)

# Create your tests here.
class StaffModelTestCase(TestCase):
    def test_current_commission(self):
        staff_1 = Staff(name='A', position='B')
        staff_1.save()

        com_1 = create_commission(10, 0, staff_1)
        com_1.save()
        self.assertEqual(staff_1.current_commission, 10)

        com_2 = create_commission(15, 1, staff_1)
        com_2.save()
        self.assertEquals(staff_1.current_commission, 15)

class SaleModelTestCase(TestCase):
    def setUp(self):
        time = timezone.now()

        staff = Staff(name="C", position="B")
        staff.save()

        product = LemonadeProduct(name="Lemonade", price=20)
        product.save()

        sale_1 = Sale(staff_id=staff, product_id=product, quantity=1)
        sale_1.save()

        sale_2 = Sale(staff_id=staff, product_id=product, quantity=2)
        one_week = timezone.now() + datetime.timedelta(days=7)
        sale_2.save()
        sale_2.date_sale = one_week
        sale_2.save()

    def test_get_staff_commission(self):
        test_sale_1 = Sale.objects.get(quantity=1)
        test_sale_2 = Sale.objects.get(quantity=2)

        staff = Staff.objects.get(name="C")

        first_commission = create_commission(10, 0, staff)
        first_commission.save()

        self.assertEquals(test_sale_1.get_staff_commission, "2")
        self.assertEquals(test_sale_2.get_staff_commission, "4")

        second_commission = create_commission(20, 7, staff)
        second_commission.save()

        self.assertEquals(test_sale_1.get_staff_commission, "2")
        self.assertEquals(test_sale_2.get_staff_commission, "8")
