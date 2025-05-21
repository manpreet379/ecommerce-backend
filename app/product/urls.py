from django.urls import path
from .views import CategoryListCreateAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),]
