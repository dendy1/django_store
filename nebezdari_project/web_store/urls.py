from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from web_store.views import AdminViews, CategoryViews, SaleViews, SellerViews

urlpatterns = [
    path('sale/create', SaleViews.SaleCreate.as_view(), name='sale_create'),

    path('sale/<int:pk>', SaleViews.SaleDetail.as_view(), name='sale_detail'),
    path('sale/<int:pk>/update', SaleViews.SaleUpdate.as_view(), name='sale_update'),
    path('sale/<int:pk>/delete', SaleViews.SaleDelete.as_view(template_name='web_store/base_confirm_delete.html'), name='sale_delete'),

    path('seller/<int:pk>', SellerViews.SellerDetail.as_view(), name='seller_detail'),
    path('seller/<int:pk>/update', SellerViews.SellerUpdate.as_view(), name='seller_update'),
    path('seller/<int:pk>/delete', SellerViews.SellerDelete.as_view(template_name='web_store/base_confirm_delete.html'), name='seller_delete'),

    path('category/create', CategoryViews.CategoryCreate.as_view(), name='category_create'),
    path('category/<int:pk>', CategoryViews.CategoryDetail.as_view(), name='category_detail'),
    path('category/<int:pk>/update', CategoryViews.CategoryUpdate.as_view(), name='category_update'),
    path('category/<int:pk>/delete', CategoryViews.CategoryDelete.as_view(template_name='web_store/base_confirm_delete.html'), name='category_delete'),

    path('admin/categories', AdminViews.AdminCategoryView.as_view(), name='admin_category_list'),
    path('admin/sales', AdminViews.AdminSaleView.as_view(), name='admin_sale_list'),
    path('admin/sellers', AdminViews.AdminSellerView.as_view(), name='admin_seller_list'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)