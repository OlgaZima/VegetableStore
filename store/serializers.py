from rest_framework import serializers
from .models import Cart, WishListTwo


class CartSerializer(serializers.ModelSerializer):
   class Meta:
       model = Cart
       fields = '__all__'


class WishListTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListTwo
        fields = '__all__'
