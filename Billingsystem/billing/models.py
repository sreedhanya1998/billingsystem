from django.db import models

# Create your models here.
class Item(models.Model):
    item_name=models.CharField(max_length=120,unique=True)

    def __str__(self):
        return self.item_name

class Purchase(models.Model):
    item_name=models.ForeignKey(Item,on_delete=models.CASCADE)
    qty_purchase=models.CharField(max_length=120)
    purchase_price=models.CharField(max_length=50)
    selling_price=models.FloatField()
    date=models.DateField()

    def __str__(self):
        return str(self.qty_purchase + self.selling_price)
class Order(models.Model):
    billnumber=models.CharField(max_length=120,unique=True)
    bill_date=models.DateField(auto_now=True)
    customer_name=models.CharField(max_length=60)
    phone_number=models.CharField(max_length=12)
    bill_total=models.IntegerField(default=0)

    def __str__(self):
        return str(self.billnumber)

class OrderLines(models.Model):
    bill_number=models.ForeignKey(Order,on_delete=models.CASCADE)
    product_name=models.ForeignKey(Item,on_delete=models.CASCADE)
    product_qty=models.FloatField()
    amount=models.CharField(max_length=120)


    def __str__(self):
        return str(self.bill_number+self.amount+self.product_qty)