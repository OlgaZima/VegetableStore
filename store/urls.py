from django.urls import path
from .views import CartView, ProductSingle, ShopView, CartViewSet, WishListView, WishlistViewCart, WishListTwoViewSet

from rest_framework import routers
app_name = 'store'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('product/<int:id>/', ProductSingle.as_view(), name='product'),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('', ShopView.as_view(), name='shop'),
    path('wish/<int:product_id>', WishlistViewCart.as_view(), name='wish')
]

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)
router.register(r'wishlist', WishListTwoViewSet)

