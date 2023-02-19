from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField
from django.urls import reverse
from django.utils import timezone, text
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import datetime
import random
import string


_ = lambda x: x

from Hotel.models import Branch, Eatery, FoodProduct

class User(models.Model):
    class Meta:
        db_table = "eaterlier_USERs"

    def __str__(self):
        return f"User : {self.user_name}"
    user_id = models.CharField(max_length=500,unique=True, primary_key=True)
    #store who is the user.
    is_manager = models.BooleanField('Manager status', default=False)
    is_staff = models.BooleanField('Staff status', default=False)
    is_customer = models.BooleanField('Customer status', default=False)
    user_name = models.CharField(max_length=30,verbose_name="user_name",blank=True)
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    user_phone = models.CharField(max_length=15, unique=True, null=True, verbose_name="Telephone number")
    user_gender = models.CharField(max_length=15, verbose_name="Gender")
    user_password = models.TextField(max_length=200,verbose_name="Password")
    user_address = models.TextField(max_length=200,verbose_name="Address")
    user_state = models.TextField(max_length=200,verbose_name="State")
    user_country = models.TextField(max_length=200,verbose_name="Country")
    date_added = models.DateTimeField(default=timezone.now)


class Customer(models.Model):
    class Meta:
        db_table = "eaterlier_Customers"
    def __str__(self):
        return f"Customer : {self.user.user_name}"
    customer_id = models.CharField(max_length=500, primary_key=True, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer')


class Manager(models.Model):
    class Meta:
        db_table = "eaterlier_Managers"
    def __str__(self):
        return f"Manager : {self.user.user_name}"
    manager_id = models.CharField(max_length=100, primary_key=True, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='manager')
    branch_ref = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branchManager')




class Staff(models.Model):
    class Meta:
        db_table = "eaterlier_Staffs"
    def __str__(self):
        return f"Staffs : {self.user.user_name}"
    staff_id = models.CharField(max_length=100, primary_key=True, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='staff')
    branch_ref = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='staffBranch')
    jobtitle = models.CharField(max_length=200,verbose_name="Title")
    work_shift = models.CharField(max_length=200,verbose_name="shift")




class otp(models.Model):
    class Meta:
        db_table = "eaterlier_OTP_Code"
    def __str__(self):
        return f"OTP FOR  : {self.user.user_name}"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.TextField(max_length=20,verbose_name="OTP CODE")
    validated = models.BooleanField(default=False)
    password_reset_code = models.TextField(max_length=20,verbose_name="Reset Code",default="")
    date_added = models.DateTimeField(default=timezone.now)


class Order(models.Model):
    class Meta:
        db_table = "eaterlier_Orders"
    def __str__(self):
        return f"Order FOR  : {self.customer_id.user.user_name}"

    order_id = models.CharField(max_length=100, primary_key=True, unique=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customerOrders')
    date_created = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_to_be_delivered = models.BooleanField(max_length=100, default=True)
    comments = models.CharField(max_length=500, blank=True)


class OrderProduct(models.Model):
    class Meta:
        db_table = "eaterlier_ProductOrders"
    def __str__(self):
        return f"Product Order FOR  : {self.order_ref.customer_id.user.user_name}"

    order_product_id = models.CharField(max_length=100, primary_key=True, unique=True)
    order_ref = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='RefOrdered')
    product_ref = models.ForeignKey(FoodProduct, on_delete=models.CASCADE, related_name='productordered')
    quantity = models.PositiveIntegerField(default=1)



class Payment(models.Model):
    class Meta:
        db_table = "eaterlier_orderPayments"
    def __str__(self):
        return f"Payment for Order: {self.order_ref.order_id}"

    payment_id = models.CharField(max_length=100, primary_key=True, unique=True)
    order_red = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='paymentOrder')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
