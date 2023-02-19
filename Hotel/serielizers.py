from rest_framework import serializers
from .models import Eatery, Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        depth =3
