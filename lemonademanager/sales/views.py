from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Sum

from .models import LemonadeProduct, Sale
from .forms import SalesForm, ReportForm
from decimal import Decimal
# Create your views here.

class SaleList:
    def __init__(self):
        self.list = []
        self.id = 0

    def appendSale(self, pid, count):
        self.list.append({'id': self.id, 'product_id': pid, "quantity": count})
        self.id = self.id + 1

    def clearSales(self):
        self.id = 0;
        self.list.clear();

    def toListRepresentation(self):
        return self.list;

    def removeSale(self, id):
        for sale in self.list:
            if sale.get("id") == id:
                self.list.remove(sale)

goba_sale_list = SaleList();

def index(request):
    return render(request, 'sales/index.html')

def form(request):
    if request.method == "POST":
        form = SalesForm(request.POST)
        if form.is_valid():
            messages.success(request, "Sale submission successfully.")
            form.save()
            staff = form.cleaned_data['staff']
            sales = goba_sale_list.toListRepresentation()

            for sale in sales:
                product_id = sale.get('product_id')
                product_ins = LemonadeProduct.objects.get(pk=product_id)
                quantity = sale.get('quantity')
                s = Sale(staff=staff, product=product_ins, quantity=quantity)
                s.save()

            return redirect("sales:form")
    else:
        form = SalesForm()

    goba_sale_list.clearSales()

    return render(request, 'sales/form.html', {'form': form})

def add(request):
    if request.method == "GET":
        product_id = request.GET.get("product")
        quantity = request.GET.get("quantity")

        product = LemonadeProduct.objects.get(pk=product_id)
        sale_id = goba_sale_list.id
        goba_sale_list.appendSale(product_id, quantity)

        sale_dict = {
            'product': product.name,
            'quantity': quantity,
            'id': sale_id,
        }

        return JsonResponse(sale_dict)

def remove(request):
    if request.method == "GET":
        goba_sale_id = request.GET.get("id")
        goba_sale_list.removeSale(goba_sale_id)

        return HttpResponse(goba_sale_id)

def report(request):
    context = {}
    if request.method == "POST":
        form = ReportForm(request.POST)
        context = {'form': form}

        # If the form is valid, get the history of the sales of that staff
        # with staff_id and in range of start_date and end_date
        #  (start_date <= dates in history <= end_date)
        if form.is_valid():
            staff = form.cleaned_data['staff']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            sales_report = Sale.objects.filter(
                staff=staff,
                date_sale__gte=start_date,
                date_sale__lte=end_date,
            ).order_by("date_sale")

            # Retrieve the overall price of all items
            # and the overall commission the staff earns
            total_overall_price = 0
            total_overall_commission = 0
            modified_sale_report = []
            no_history_message = ""

            # Modifying the report
            if sales_report:
                sale_dict = {}
                first_sale = sales_report[0]
                sale_dict['date'] = first_sale.date_sale
                sale_dict['list_of_products'] = "{} {}".format(str(first_sale.quantity), str(first_sale.product))
                sale_dict['total_price'] = Decimal(first_sale.get_price)
                sale_dict['commission'] = Decimal(first_sale.get_staff_commission)
                modified_sale_report.append(sale_dict)

                for sale in sales_report:
                    total_overall_price += Decimal(sale.get_price)
                    total_overall_commission += Decimal(sale.get_staff_commission)

                    temp_sale = {}
                    latest_sale = modified_sale_report[-1]
                    if sale != sales_report[0]:
                        if (sale.date_sale - latest_sale['date']).total_seconds() <= 59:
                            temp_sale['list_of_products'] = latest_sale['list_of_products'] + ", " + "{} {}".format(str(sale.quantity), str(sale.product))
                            temp_sale['total_price'] = latest_sale['total_price'] + Decimal(sale.get_price)
                            temp_sale['commission'] = latest_sale['commission'] + Decimal(sale.get_staff_commission)
                            latest_sale.update(temp_sale)
                        else:
                            temp_sale['date'] = sale.date_sale
                            temp_sale['list_of_products'] = "{} {}".format(str(sale.quantity), str(sale.product))
                            temp_sale['total_price'] = Decimal(sale.get_price)
                            temp_sale['commission'] = Decimal(sale.get_staff_commission)
                            modified_sale_report.append(temp_sale)

            # If there's no records, print the notification message
            else:
                no_history_message = "There's no records for this staff between the given times."

            context = {
                'form': form,
                # 'sales_report': sales_report,
                'total_overall_price'       : total_overall_price,
                'total_overall_commission'  : total_overall_commission,
                'modified_sale_report'      : modified_sale_report,
                'no_history_message'        : no_history_message
            }
    else:
        form = ReportForm()
        context = {'form': form}
    return render(request, 'sales/report.html', context)
