from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from web_store import views

urlpatterns = [
    path('sale/create', views.SaleCreate.as_view(), name='sale_create'),

    path('sale/<int:pk>', views.SaleDetail.as_view(), name='sale_detail'),
    path('sale/<int:pk>/update', views.SaleUpdate.as_view(), name='sale_update'),
    path('sale/<int:pk>/delete', views.SaleDelete.as_view(), name='sale_delete'),

    path('seller/<int:pk>', views.SellerDetail.as_view(), name='seller_detail'),
    path('seller/<int:pk>/update', views.SellerUpdate.as_view(), name='seller_update'),
    path('seller/<int:pk>/delete', views.SellerDelete.as_view(), name='seller_delete'),

    path('category/create', views.CategoryCreate.as_view(), name='category_create'),
    path('category/<int:pk>', views.CategoryDetail.as_view(), name='category_detail'),
    path('category/<int:pk>/update', views.CategoryUpdate.as_view(), name='category_update'),
    path('category/<int:pk>/delete', views.CategoryDelete.as_view(), name='category_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)