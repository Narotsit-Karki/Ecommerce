from .models import Product
from rest_framework import serializers

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__" # to add all fields in the models