from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings  # Новый импорт
from django.conf.urls.static import static  # Новый импорт

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # Регистрация и профиль пользователя
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # Работа с предложениями (offers)
    path('create-offer/', views.create_offer, name='create_offer'),
    path('edit-offer/<int:offer_id>/', views.edit_offer, name='edit_offer'),
    path('delete-offer/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('join-offer/<int:offer_id>/', views.join_offer, name='join_offer'),
    
    # Работа с постами (posts)
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    
    # Сообщения
    path('inbox/', views.inbox, name='inbox'),
    path('send-message/<int:receiver_id>/', views.send_messages, name='send_message'),
    path('archive-message/<int:message_id>/', views.archive_message, name='archive_message'),
    path('unarchive-message/<int:message_id>/', views.unarchive_message, name='unarchive_message'),
    path('users/', views.users_list, name='users_list'),  # Список пользователей
    
    # Календарь и события
    path('get-events/', views.get_events, name='get_events'),
    path('add-event/', views.add_event, name='add_event'),
    path('update-event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    
    # Комментарии и рейтинги
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('add-rating/<int:post_id>/', views.add_rating, name='add_rating'),
    
    # Страницы с условиями использования и политикой конфиденциальности
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logget_out.html'), name='logout'),
    
    # Сброс пароля
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]

# Добавляем обработку медиафайлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
