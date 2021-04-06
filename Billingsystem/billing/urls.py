"""Billingsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .views import create_bill,purchase_list,purchase_view,purchase_edit,purchase_delete,Ordercreate,Orderline,Billgenerate,Registration,loginView,Datewise
urlpatterns = [
 path('', lambda request: render(request, "billing/base.html")),
   path("item",create_bill.as_view(),name="item"),
    path("list",purchase_list.as_view(),name="list"),
    path("view/<int:pk>",purchase_view.as_view(),name="view"),
    path("edit/<int:pk>",purchase_edit.as_view(),name="edit"),
    path("delete/<int:pk>",purchase_delete.as_view(),name="delete"),
    path("order",Ordercreate.as_view(),name="order"),
 path("orderline/<str:billnumber>",Orderline.as_view(),name="orderline"),
 path('billgenerate/<str:billnumber>',Billgenerate.as_view(),name="billgenerate"),
 path("register",Registration.as_view(),name="register"),
 path("login",loginView.as_view(),name="login"),
 path("date",Datewise.as_view(),name="date")
]
