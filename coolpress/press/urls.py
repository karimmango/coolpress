from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='posts_list'),
    path('post/<int:post_id>/', views.post_detail, name='posts_detail'),
]