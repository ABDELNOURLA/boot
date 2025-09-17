from django.urls import path
from . import views

urlpatterns =[
    path("webhook/", views.productList.as_view(), name="webhook"),
]