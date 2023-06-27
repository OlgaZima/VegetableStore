from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField, Case, When
from django.utils import timezone
from .models import Product, Discount, Cart, WishListTwo, Profile
from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer

# Create your views here.

class CartView(View):
    def get(self, request):
        return render(request, 'store/cart.html')


class ProductSingle(View):
    def get(self, request, id):
        data = Product.objects.get(id=id)
        # data = {1: {'name': 'Bell Pepper',
        #             'description': 'Bell Pepper',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-1.jpg'},
        #         2: {'name': 'Strawberry',
        #             'description': 'Strawberry',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-2.jpg'},
        #         3: {'name': 'Green Beans',
        #             'description': 'Green Beans',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-3.jpg'},
        #         4: {'name': 'Purple Cabbage',
        #             'description': 'Purple Cabbage',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-4.jpg'},
        #         5: {'name': 'Tomatoe',
        #             'description': 'Tomatoe',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-5.jpg'},
        #         6: {'name': 'Brocolli',
        #             'description': 'Brocolli',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-6.jpg'},
        #         7: {'name': 'Carrots',
        #             'description': 'Carrots',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-7.jpg'},
        #         8: {'name': 'Fruit Juice',
        #             'description': 'Fruit Juice',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-8.jpg'},
        #         9: {'name': 'Onion',
        #             'description': 'Onion',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-9.jpg'},
        #         10: {'name': 'Apple',
        #              'description': 'Apple',
        #              'price': 120.00,
        #              'rating': 5.0,
        #              'url': 'store/images/product-10.jpg'},
        #         11: {'name': 'Garlic',
        #              'description': 'Garlic',
        #              'price': 120.00,
        #
        #              'rating': 5.0,
        #              'url': 'store/images/product-11.jpg'},
        #         12: {'name': 'Chilli',
        #              'description': 'Chilli',
        #              'price': 120.00,
        #              'rating': 5.0,
        #              'url': 'store/images/product-12.jpg'}
        #         }
        # return render(request, "store/product-single.html", context=data[id])
        # data = Product.objects.get(id=id)
        return render(request,
                      "store/product-single.html",
                      context={'name': data.name,
                               'description': data.description,
                               'price': data.price,
                               'rating': 5.0,
                               'url': data.image.url,
                               })

# class Shop(View):
#     def get(self, request):
#         return render(request, 'store/shop.html')


class ShopView(View):
    def get(self, request):
        # Создание запроса на получения всех действующих не нулевых скидок
        discount_value = Case(When(discount__value__gte=0,
                                   discount__date_begin__lte=timezone.now(),
                                   discount__date_end__gte=timezone.now(),
                                   then=F('discount__value')),
                              default=0,
                              output_field=DecimalField(max_digits=10, decimal_places=2)
                              )
        # Создание запроса на расчёт цены со скидкой
        price_with_discount = ExpressionWrapper(
            F('price') * (100.0 - F('discount_value')) / 100.0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )

        products = Product.objects.annotate(
            discount_value=discount_value,
            # Другой способ через запрос в другую таблицу, однако
            # без фильтрации по времени действия скидки
            # discount_value=Subquery(
            #     Discount.objects.filter(product_id=OuterRef('id')).values(
            #         'value')
            # ),
            price_before=F('price'),
            price_after=price_with_discount
        ).values('id', 'name', 'image', 'price_before', 'price_after',
                 'discount_value')
        return render(request, 'store/shop.html', {"data": products})

    # def get(self, request):
    #     context = {'data': [{'name': 'Bell Pepper',
    #                          'discount': 30,
    #                          'price_before': 120.00,
    #                          'price_after': 80.00,
    #                          'url': 'store/images/product-1.jpg',
    #                          'id': 1},
    #                         {'name': 'Strawberry',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-2.jpg',
    #                          'id': 2},
    #                         {'name': 'Green Beans',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-3.jpg',
    #                          'id': 3},
    #                         {'name': 'Purple Cabbage',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-4.jpg',
    #                          'id': 4},
    #                         {'name': 'Tomatoe',
    #                          'discount': 30,
    #                          'price_before': 120.00,
    #                          'price_after': 80.00,
    #                          'url': 'store/images/product-5.jpg',
    #                          'id': 5},
    #                         {'name': 'Brocolli',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-6.jpg',
    #                          'id': 6},
    #                         {'name': 'Carrots',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-7.jpg',
    #                          'id': 7},
    #                         {'name': 'Fruit Juice',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-8.jpg',
    #                          'id': 8},
    #                         {'name': 'Onion',
    #                          'discount': 30,
    #                          'price_before': 120.00,
    #                          'price_after': 80.00,
    #                          'url': 'store/images/product-9.jpg',
    #                          'id': 9},
    #                         {'name': 'Apple',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-10.jpg',
    #                          'id': 10},
    #                         {'name': 'Garlic',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-11.jpg',
    #                          'id': 11},
    #                         {'name': 'Chilli',
    #                          'discount': None,
    #                          'price_before': 120.00,
    #                          'url': 'store/images/product-12.jpg',
    #                          'id': 12},
    #                         ]
    #                }
    #     return render(request, 'store/shop.html', context)


class CartViewSet(viewsets.ModelViewSet):
  queryset = Cart.objects.all()
  serializer_class = CartSerializer
  permission_classes = (IsAuthenticated,)


  def get_queryset(self):
      return self.queryset.filter(user=self.request.user)

  def create(self, request, *args, **kwargs):
      ## Можно записать так, для получения товара (проверка что он уже есть в корзине)
      # cart_items = Cart.objects.filter(user=request.user,
      #                                  product__id=request.data.get('product'))
      # Или можно так, так как мы переопределили метод get_queryset
      cart_items = self.get_queryset().filter(product__id=request.data.get('product'))
      # request API передаёт параметры по названиям полей в БД, поэтому ловим product
      if cart_items:  # Если продукт уже есть в корзине
          cart_item = cart_items[0]
          if request.data.get('quantity'):  # Если в запросе передан параметр quantity,
              # то добавляем значение к значению в БД
              cart_item.quantity += int(request.data.get('quantity'))
          else:  # Иначе просто добавляем значение по умолчению 1
              cart_item.quantity += 1
      else:  # Если продукта ещё нет в корзине
          product = get_object_or_404(Product, id=request.data.get('product'))  # Получаем продукт и
          # проверяем что он вообще существует, если его нет то выйдет ошибка 404
          if request.data.get('quantity'):  # Если передаём точное количество продукта, то передаём его
              cart_item = Cart(user=request.user, product=product, quantity=request.data.get('quantity'))
          else:  # Иначе создаём объект по умолчанию (quantity по умолчанию = 1, так прописали в моделях)
              cart_item = Cart(user=request.user, product=product)
      cart_item.save()  # Сохранили объект в БД
      return response.Response({'message': 'Product added to cart'}, status=201)  # Вернули ответ, что всё прошло успешно

  def update(self, request, *args, **kwargs):
      # Для удобства в kwargs передаётся id строки для изменения в БД, под параметром pk
      cart_item = get_object_or_404(Cart, id=kwargs['pk'])
      if request.data.get('quantity'):
          cart_item.quantity = request.data['quantity']
      if request.data.get('product'):
          product = get_object_or_404(Product, id=request.data['product'])
          cart_item.product = product
      cart_item.save()
      return response.Response({'message': 'Product change to cart'}, status=201)

  def destroy(self, request, *args, **kwargs):
      # В этот раз напишем примерно так как это делает фреймфорк самостоятельно
      cart_item = self.get_queryset().get(id=kwargs['pk'])
      cart_item.delete()
      return response.Response({'message': 'Product delete from cart'}, status=201)


class WishListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            products = WishListTwo.objects.filter(userwish__user=request.user)
            #products = WishListTwo.objects.all()
            return render(request, 'store/wishlist.html', {"data": products})
        else:
            return redirect('login:login')


class WishlistViewCart(View):
    def get(self, request, product_id):
        wishlist = WishListTwo.objects.filter(userwish__user=request.user, product__id=product_id)
        if wishlist:
            wishlist_item = wishlist[0]
            wishlist_item.quantity += 1
        else:
            product = get_object_or_404(Product, id=product_id)
            user = get_object_or_404(WishListTwo, userwish__user=request.user)
            wishlist_item = WishListTwo(wishlist=user, product=product)
        wishlist_item.save()
        return redirect('store:wishlist')




