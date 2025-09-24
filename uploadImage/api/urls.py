from django.urls import path
from uploadImage.api import views

urlpatterns = [
    path('upload/image/', views.UploadImage.as_view(), name='blog_user_list'),
]
