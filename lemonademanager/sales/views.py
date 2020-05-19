from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum

from .models import LemonadeProduct, Sale
from .forms import SalesForm, ReportForm
from decimal import Decimal
# Create your views here.


def index(request):
    return render(request, 'sales/index.html')

def form(request):
    if(request.method == "POST"):
        form = SalesForm(request.POST)
        if form.is_valid():
            messages.success(request, "Sale submission successfully.")
            form.save()
            return redirect("sales:form")

    else:
        form = SalesForm()

    return render(request, 'sales/form.html', {'form': form})

def report(request):
    context = {}
    if(request.method == "POST"):
        form = ReportForm(request.POST)
        context = {'form': form}

        # If the form is valid, get the history of the sales of that staff
        # with staff_id and in range of start_date and end_date
        #  (start_date <= dates in history <= end_date)
        if form.is_valid():
            staff_id = form.cleaned_data['staff_id']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            sales_report = Sale.objects.filter(
                staff_id=staff_id,
                date_sale__gte=start_date,
                date_sale__lte=end_date,
            ).order_by("date_sale")

            # Retrieve the overall price of all items
            # and the overall commission the staff earns
            total_overall_price = 0
            total_overall_commission = 0

            # modified_sale_report = []

            for sale in sales_report:
                total_overall_price += Decimal(sale.get_price)
                total_overall_commission += Decimal(sale.get_staff_commission)


            context = {
                'form': form,
                'sales_report': sales_report,
                'total_overall_price': total_overall_price,
                'total_overall_commission': total_overall_commission
            }
    else:
        form = ReportForm()
        context = {'form': form}
    return render(request, 'sales/report.html', context)
