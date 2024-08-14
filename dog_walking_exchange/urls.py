# dog_walking_exchange/urls.py

from django.contrib import admin
from django.urls import path, include
from users import views  # Импортируем представления из приложения users
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Включение URL-адресов приложения users
    path('accounts/', include('django.contrib.auth.urls')),  # Подключение стандартных URL-ов аутентификации
    path('accounts/', include('allauth.urls')),  # Подключение URL-ов для allauth (если используется)
    path('', views.home, name='home'),  # Главная страница
]

# Подключение медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
