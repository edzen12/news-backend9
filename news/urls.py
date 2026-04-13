from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from post import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),
    path('currency/', views.currency_view, name='currency'),
    path('tags/<slug:slug>', views.tag_posts, name='tag_posts'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
