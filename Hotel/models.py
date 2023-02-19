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



class Eatery(models.Model):
    class Meta:
        db_table = "eaterlier_Eterly"
    def __str__(self):
        return f"Eatery: {self.name}"

    eatery_id = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Eatery/')
    is_verified = models.BooleanField(default=False)
    verification_code = models.TextField(max_length=20,verbose_name="VERIFICATION CODE", default=0000)
    email = models.CharField(max_length=100, unique=True, blank=False, default='admin@email.com')
    password = models.TextField(max_length=200,verbose_name="Password", default='password')
    registered_date = models.DateTimeField(default=timezone.now)


class Branch(models.Model):
    class Meta:
        db_table = "eaterlier_Branch"
    def __str__(self):
        return f"Branch: {self.name} for Eatery {self.branch_ref.name}"

    branch_id = models.CharField(max_length=100, primary_key=True, unique=True)
    branch_ref = models.ForeignKey(Eatery, on_delete=models.CASCADE, related_name='branchREF')
    name = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    registered_date = models.DateTimeField(default=timezone.now)


class FoodCategory(models.Model):
    class Meta:
        db_table = "eaterlier_FoodCategory"
    def __str__(self):
        return f"Category: {self.name}"

    food_category_id = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100, default='uncategorised')
    description = models.CharField(max_length=100, blank=True)
    branchID = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='BranchFoodCategory')


class FoodSubCategory(models.Model):
    class Meta:
        db_table = "eaterlier_FoodSubCategory"
    def __str__(self):
        return f"Sub Category: {self.name}"

    food_subcategory_id = models.CharField(max_length=100, primary_key=True, unique=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='FoodSubCategory')
    name = models.CharField(max_length=100, default='uncategorised')
    description = models.CharField(max_length=100, blank=True)


class FoodProduct(models.Model):
    class Meta:
        db_table = "eaterlier_FoodProduct"
    def __str__(self):
        return f"FoodProduct: {self.name}"

    food_product_id = models.CharField(max_length=100, primary_key=True, unique=True)
    subcategory = models.ForeignKey(FoodSubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_products/')
    quantityAvailable = models.PositiveIntegerField()
