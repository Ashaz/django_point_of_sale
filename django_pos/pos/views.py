import json
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.shortcuts import render
from products.models import Product, Category
from sales.models import Sale
import numpy as np


# @login_required(login_url="/accounts/login/")
# def index(request):
#     today = date.today()
#
#     year = today.year
#     monthly_earnings = []
#
#     # Calculate earnings per month
#     for month in range(1, 13):
#         earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
#             total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
#         monthly_earnings.append(earning)
#
#     # Calculate annual earnings
#     annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(total_variable=Coalesce(
#         Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
#     annual_earnings = format(annual_earnings, '.2f')
#
#     # AVG per month
#     avg_month = format(sum(monthly_earnings)/12, '.2f')
#
#     # Top-selling products
#     top_products = Product.objects.annotate(quantity_sum=Sum(
#         'saledetail__quantity')).order_by('-quantity_sum')[:3]
#
#     top_products_names = []
#     top_products_quantity = []
#
#     for p in top_products:
#         top_products_names.append(p.name)
#         top_products_quantity.append(p.quantity_sum)
#
#     print(top_products_names)
#     print(top_products_quantity)
#
#     context = {
#         "active_icon": "dashboard",
#         "products": Product.objects.all().count(),
#         "categories": Category.objects.all().count(),
#         "annual_earnings": annual_earnings,
#         "monthly_earnings": json.dumps(monthly_earnings),
#         "avg_month": avg_month,
#         "top_products_names": json.dumps(top_products_names),
#         "top_products_names_list": top_products_names,
#         "top_products_quantity": json.dumps(top_products_quantity),
#     }
#     return render(request, "pos/index.html", context)

@login_required(login_url="/accounts/login/")
def index(request):
    # Start date and weekly_predictions variable
    start_date = date(2024, 4, 8)
    weekly_predictions = []



    # Generate predictions for 6 weeks
    for week in range(6):
        week_start = start_date + timedelta(weeks=week)  # Calculate a new date by adding duration to start date

        p = np.random.uniform(10, 100)  # Get random average price
        f = np.random.uniform(1000, 5000)  # Get random fixed costs between 1000 and 5000
        r = np.random.uniform(0.01, 0.2)  # Get random conversion rate between 1% and 20%
        v = np.random.randint(100, 1000)  # Get random leads volume between 100 and 1000
        c = np.random.randint(1, 10)  # Get random competitor index between 1 and 10
        d = np.random.randint(1, 10)  # Get random demand index between 1 and 10
        a = np.random.randint(10, 100)  # Get random number of sales between 10 and 100

        # Utilise prediction formula
        prediction = ((p * a) / 6) * (d / c) * ((1 + (v / 1000)) * r) - (f / 6)
        prediction = abs(prediction)
        weekly_predictions.append({
            "week_start": week_start.strftime('%Y-%m-%d'),
            "prediction": prediction
        })

    today = date.today()

    year = today.year
    monthly_earnings = []

    # Calculate earnings per month
    for month in range(1, 13):
        earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
            total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
        monthly_earnings.append(earning)

    # Calculate annual earnings
    annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(total_variable=Coalesce(
        Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
    annual_earnings = format(annual_earnings, '.2f')

    # AVG per month
    avg_month = format(sum(monthly_earnings)/12, '.2f')

    # Top-selling products
    top_products = Product.objects.annotate(quantity_sum=Sum(
        'saledetail__quantity')).order_by('-quantity_sum')[:3]

    top_products_names = []
    top_products_quantity = []

    for p in top_products:
        top_products_names.append(p.name)
        top_products_quantity.append(p.quantity_sum)

    print(top_products_names)
    print(top_products_quantity)

    context = {
        "active_icon": "dashboard",
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),
        "weekly_predictions": json.dumps(weekly_predictions),
    }
    print(json.dumps(weekly_predictions))
    return render(request, "pos/index.html", context)
