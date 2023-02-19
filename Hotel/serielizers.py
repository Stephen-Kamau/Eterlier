from rest_framework import serializers
from .models import Eatery, Branch, FoodCategory, FoodSubCategory, FoodProduct

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        depth =3


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = "__all__"
        depth =3


class FoodSUBCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodSubCategory
        fields = "__all__"
        depth =3

class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = "__all__"
        depth =3
