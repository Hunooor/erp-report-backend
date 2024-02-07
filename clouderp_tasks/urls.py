from django.urls import path

from clouderp_tasks.views import get_blocked_assets, get_customer_report, get_product_report, save_product

urlpatterns = [
    path("report/order/", get_blocked_assets),
    path("report/customer/", get_customer_report),
    path("report/product/", get_product_report),
    path("product/", save_product),
]
