from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MenuItem(models.Model):
    category = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2, max_digits=4)
    large_price = models.DecimalField(
        decimal_places=2, max_digits=4, null=True)

    def __str__(self):
        return f"{self.description} {self.category}"


class Topping(models.Model):
    description = models.CharField(max_length=64)
    allowed_subs = models.NullBooleanField()

    def __str__(self):
        if self.allowed_subs is not None:
            return f"{self.description}, Allowed on Subs"

        return f"{self.description}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    item_count = models.IntegerField(default=0)
    checked_out = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    check_out_date = models.DateTimeField(null=True)
    completed_date = models.DateTimeField(null=True)

    def __str__(self):
        if not self.checked_out:
            return f"Order ID#:{self.id}, For {self.user}, Not Checked Out"
        else:
            return f"Order ID#:{self.id}, For {self.user}, Checked out on {self.check_out_date}"


class Order_item(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, null=True)
    extras = models.CharField(max_length=255, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return f"{self.item_id} {self.size}, Price: ${self.price}, Extras: {self.extras}"
