from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path("contact/", views.contact, name="contact"),
    path('api/product/<int:pk>/', views.product_detail_json, name='product_detail_json'),
]
