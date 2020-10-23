from django.urls import path

from web_store import views

urlpatterns = [
    path('sale/create', views.SaleCreate.as_view(), name='sale_create'),

    path('sale/<pk>', views.SaleDetail.as_view(), name='sale_detail'),
    path('sale/<pk>/update', views.SaleUpdate.as_view(), name='sale_update'),
    path('sale/<pk>/delete', views.SaleDelete.as_view(), name='sale_delete'),

    path('seller/<pk>', views.SellerDetail.as_view(), name='seller_detail'),
    path('seller/<pk>/update', views.SellerUpdate.as_view(), name='seller_update'),
    path('seller/<pk>/delete', views.SellerDelete.as_view(), name='seller_delete'),

    path('category/<pk>', views.CategoryDetail.as_view(), name='category_detail'),
    path('category/<pk>/update', views.CategoryUpdate.as_view(), name='category_update'),
    path('category/<pk>/delete', views.CategoryDelete.as_view(), name='category_delete'),
]