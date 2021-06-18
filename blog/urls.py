from django.urls import path, include

from .views import article_list, article_detail, category_list, register_user, login_user, logout_user

urlpatterns = [
    path('', article_list, name='article_list'),
    path('articles/<slug:slug>/', article_detail, name='article_detail'),
    path('category/<slug:slug>/', category_list, name='category_list'),
    path('register/', register_user, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
]
