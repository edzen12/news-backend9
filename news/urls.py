from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from post import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
