from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid


def create_rand_id():
        from django.utils.crypto import get_random_string
        return get_random_string(length=13, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


class ExpensesCategory(models.Model):
    category = models.CharField(max_length=255)

    
    def __str__(self):
        return f"{self.category}".title()

class Keywords(models.Model):
    category = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE, null=True, blank=True)
    keywords = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.keywords}"

class Uploaded_Image_Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/expenses', blank=True, null=True)
    reference_number = models.CharField(
        max_length=255, editable=False, null=True, blank=True,
        default=create_rand_id
    )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_added",)

    def __str__(self):
        return f"{self.reference_number}"
    

class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    expense_name = models.CharField(max_length=255)
    total_amount = models.FloatField(max_length=10)
    rndid = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255)

    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return f"{self.expense_name}|{self.user}|{self.total_amount}"
    
    def price(self):
        total_amount = float(self.total_amount)
        total_amountstr = "₱ {:,.2f}".format(total_amount)
        return total_amountstr

    def date(self):
        locale.setlocale(locale.LC_ALL, 'en-US')
        return self.date_added.strftime("%B %d, %Y")
    
    def get_month(self):
        import datetime
        datee = datetime.datetime.strptime(self.date_added, "%Y-%m-%d")
        return int(datee.month)