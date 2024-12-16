from django.db import models


class ProductManager(models.Manager):
    def low_stock(self, threshold=10):
        return self.filter(stock__lt=threshold)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    objects = ProductManager()

    def __str__(self):
        return self.name


class OrderQuerySet(models.QuerySet):
    def for_product(self, product_id):
        return self.filter(product_id=product_id)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = OrderQuerySet.as_manager()  # Применяем QuerySet как менеджер

    def __str__(self):
        return f"Order for {self.product.name}"
