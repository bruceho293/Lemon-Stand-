from django.urls import path

from . import views

app_name = 'sales'
urlpatterns = [
    # ex: /salesystem/
    path('', views.index, name='index'),
    # ex: /salesystem/sales/form/
    path('form', views.form, name='form'),
    # ex: /salesystem/sales/reports
    path('report', views.report, name='report')
]
