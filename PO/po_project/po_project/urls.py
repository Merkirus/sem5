"""
URL configuration for po_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from po_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('offert/', views.offert, name='offert'),
    path('basket/', views.basket, name='basket'),
    path('order/', views.order, name='order'),
    path('order/basket', views.order_basket, name='order_basket'),
    path('basket/<str:error>', views.basket, name="basket_error")
]
