from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from clouderp_tasks.models import Product
from clouderp_tasks.services import get_blocked_assets_service, get_customer_report_service, get_product_report_service, \
    save_product_service, check_or_create_product_task
from djangoProject.exceptions import BadRequestException


@api_view(['GET'])
def get_blocked_assets(request):
    return Response(data=get_blocked_assets_service(),
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def get_customer_report(request):
    return Response(data=get_customer_report_service(query_parameter_list=request.GET),
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def get_product_report(request):
    return Response(data=get_product_report_service(), status=status.HTTP_200_OK)


@api_view(['POST'])
def save_product(request):
    try:
        return Response(data=save_product_service(request_data=request.data),
                        status=status.HTTP_200_OK)
    except BadRequestException as err:
        return Response(data={"error": err.message},
                        status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=Product)
def product_post_save_check(sender, instance, created, **kwargs):
    if created or not created:
        check_or_create_product_task(product=instance)
