from django.db import transaction
from models import Product, Order
from django.http import JsonResponse


def process_order(product_id, quantity):
    try:
        with transaction.atomic():  # Начало транзакции
            product = Product.objects.select_for_update().get(id=product_id)

            if product.stock < quantity:
                raise ValueError("Insufficient stock for the product.")

            product.stock -= quantity
            product.save()

            total_price = product.price * quantity
            order = Order.objects.create(
                product=product,
                quantity=quantity,
                total_price=total_price
            )

            print("Order processed successfully!")
            return order

    except ValueError as e:
        print(f"Transaction rolled back: {e}")
        transaction.set_rollback(True)
        return None


def create_order_view(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))

        order = process_order(product_id, quantity)

        if order:
            return JsonResponse({"status": "success", "order_id": order.id})
        else:
            return JsonResponse({"status": "failure", "message": "Transaction failed."})
    return JsonResponse({"status": "error", "message": "Invalid request."})
