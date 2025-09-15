from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .api import ProductViewSet

app_name = 'products'


urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('upload/success/', views.upload_success, name='upload_success'),
]



router = DefaultRouter()
router.register(r'api/products', ProductViewSet, basename='product')

urlpatterns += router.urls