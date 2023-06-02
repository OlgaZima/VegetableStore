from django.urls import path

from.views import currentDateView, randomView, strHello, IndexView

urlpatterns = [
    path('datetime/', currentDateView.as_view()),
    path('random/', randomView.as_view()),
    path('hello/', strHello.as_view()),
    path('', IndexView.as_view())
]
