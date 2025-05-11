from django.urls import path
from authentication.api import views

urlpatterns = [
    path('user/list/', views.BlogUserList.as_view(), name='blog_user_list'),
    path('user/details/<int:id>/', views.BlogUserDetails.as_view(), name='blog_user_details'),
    path('user/login/', views.blog_user_login, name='blog_user_login'),
    path('user/logout/', views.blog_user_logout, name='blog_user_logout'),
    path('user/info/', views.user_info, name='user_info'),
]
