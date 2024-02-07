from django.db.models import Sum, F, Q, Case, Count, When

from clouderp_tasks.models import TaskStatus, Task, OrderItem, Order, Customer, Product
from djangoProject.exceptions import BadRequestException


def get_blocked_assets_service():
    open_order_tasks = TaskStatus.objects.filter(
        status_category__in=["TO_DO", "IN_PROGRESS"], task_id__in=
        Task.objects.filter(order__isnull=False).values_list("id", flat=False))

    result = OrderItem.objects.filter(
        order__in=Order.objects.filter(
            pk__in=open_order_tasks)).aggregate(
        blocked_assets_total_price=Sum("quantity"),
        blocked_assets_total_quantity=Sum(F("product__price").__mul__(F("quantity"))))

    return result


def get_customer_report_service(query_parameter_list):
    offset = 0
    limit = 10  # the offset value is defined in the design file
    query = Q()

    if "page" in query_parameter_list:
        page = query_parameter_list["page"]
        offset = (int(page) * int(limit)) - int(limit)

    if "name" in query_parameter_list:
        query &= Q(name__icontains=query_parameter_list["name"])

    customer_list = Customer.objects.filter(query)[offset:limit + offset]

    response_item_list = []
    for customer in customer_list:
        task_list = TaskStatus.objects.filter(Q(task__customer=customer) | Q(task__order__customer=customer)) \
            .aggregate(
            todo=Count(Case(When(status_category="TO_DO", then=1))),
            in_progress=Count(Case(When(status_category="IN_PROGRESS", then=1))),
            done=Count(Case(When(status_category="DONE", then=1))),
        )

        response_item = {
            "id": customer.id,
            "name": customer.name,
            "todo": task_list["todo"],
            "in_progress": task_list["in_progress"],
            "done": task_list["done"]
        }
        if "has_open_tasks" in query_parameter_list:
            if task_list["todo"] > 0 or task_list["in_progress"] > 0:
                response_item_list.append(response_item)
        else:
            response_item_list.append(response_item)

    return {"results": response_item_list}


def get_product_report_service():
    response = Product.objects.all().aggregate(
        total_products=Count("id"),
        invalid_products=Count("id",
                               filter=(
                                       Q(name__isnull=True) |
                                       Q(sku__isnull=True) |
                                       Q(price__isnull=True)))
    )

    return response


def _is_valid_product(product: Product) -> bool:
    if product.name is None or product.sku is None or product.price is None:
        return False
    return True


def _create_product_task(product: Product):
    if not TaskStatus.objects.filter(task__product=product, status_category="TO_DO") \
            .exists():
        task, created = Task.objects.update_or_create(
            product=product,
            defaults={"description": "random prod task description"}
        )

        TaskStatus.objects.create(
            name="product task name",
            task=task
        )


def _complete_product_task(product: Product):
    if _is_valid_product(product):
        TaskStatus.objects.filter(task__product=product, status_category="TO_DO") \
            .update(status_category="DONE")


def check_or_create_product_task(product: Product):
    if not _is_valid_product(product=product):
        _create_product_task(product=product)
    else:
        _complete_product_task(product=product)


def save_product_service(request_data):
    try:
        if "id" in request_data and request_data["id"] is not None:
            product = Product.objects.get(pk=request_data["id"])
            product.name = request_data["name"] if "name" in request_data else None
            product.sku = request_data["sku"] if "sku" in request_data else None
            product.price = request_data["price"] if "price" in request_data else None
            product.save()
        else:
            Product.objects.create(**request_data)

    except (ValueError, Exception) as e:
        print(e)
        raise BadRequestException("Invalid request data")
