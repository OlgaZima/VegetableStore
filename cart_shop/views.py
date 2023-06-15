from django.shortcuts import render

# Create your views here.
from django.views import View
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField, Case, When
from django.utils import timezone
from store.models import Product, Discount, Cart

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
  queryset = Cart.objects.all()
  serializer_class = CartSerializer
  permission_classes = (IsAuthenticated,)


  def get_queryset(self):
      return self.queryset.filter(user=self.request.user)

