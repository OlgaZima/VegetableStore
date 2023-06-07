from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField, Case, When
from django.utils import timezone
from .models import Product, Discount
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