from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .forms import (
    UserRegistrationForm,
    UserProfileForm,
    UserUpdateForm,
    OfferForm,
    PostForm,
    MessageForm,
    CommentForm,
    RatingForm,
    EventForm
)
from .models import (
    DogWalkingOffer,
    Message,
    UserProfile,
    Post,
    Comment,
    Rating,
    Event,
    Participation
)

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем его
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # Создаем профиль пользователя
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()

            # Аутентифицируем и логиним пользователя
            user = authenticate(username=new_user.username, password=user_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful. You are now logged in.')
                return redirect('profile')  # Перенаправляем пользователя на страницу профиля
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

# Профиль пользователя
@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)

# Отображение главной страницы с предложениями и постами
def home(request):
    offers = DogWalkingOffer.objects.all()
    posts = Post.objects.all()
    return render(request, 'home.html', {'offers': offers, 'posts': posts})

# Создание нового предложения
@login_required
@login_required
def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.owner = request.user
            offer.save()
            print(f"Offer created: {offer.title}, {offer.description}")  # Добавьте это для отладки
            messages.success(request, 'Offer created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error creating offer. Please correct the form.')
            print(form.errors)  # Отображение ошибок формы
    else:
        form = OfferForm()
    return render(request, 'users/create_offer.html', {'form': form})


# Редактирование предложения
@login_required
def edit_offer(request, offer_id):
    offer = get_object_or_404(DogWalkingOffer, id=offer_id, owner=request.user)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer updated successfully.')
            return redirect('home')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'users/edit_offer.html', {'form': form})

# Удаление предложения
@login_required
def delete_offer(request, offer_id):
    offer = get_object_or_404(DogWalkingOffer, id=offer_id, owner=request.user)
    offer.delete()
    messages.success(request, 'Offer deleted successfully.')
    return redirect('home')

# Присоединение к предложению
@login_required
def join_offer(request, offer_id):
    offer = get_object_or_404(DogWalkingOffer, id=offer_id)
    if not offer.stakeholders.filter(id=request.user.id).exists():
        offer.stakeholders.add(request.user)
        messages.success(request, 'You have successfully joined the offer.')
    else:
        messages.warning(request, 'You have already joined this offer.')
    return redirect('home')

# Создание поста
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'users/create_post.html', {'form': form})

# Редактирование поста
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'users/edit_post.html', {'form': form})

# Удаление поста
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    return redirect('home')

# Добавление комментария
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'There was an error adding your comment.')
    return redirect('home')

# Удаление комментария
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user == comment.post.author:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    return redirect('home')

# Страницы с условиями использования и политикой конфиденциальности
def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

# Работа с событиями (пример)
@login_required
def get_events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        created_by = {
            'username': event.user.username if event.user else 'Unknown',
            'avatar': event.user.userprofile.profile_picture.url if hasattr(event.user, 'userprofile') and event.user.userprofile.profile_picture else None
        }
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat() if event.end_date else None,
            'location': event.location,
            'description': event.description,
            'created_by': created_by
        })
    return JsonResponse(event_list, safe=False)

@csrf_exempt
@login_required
def add_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event = Event(
            title=data.get('title'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            location=data.get('location'),
            description=data.get('description'),
            user=request.user
        )
        event.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@require_http_methods(["POST"])
@csrf_exempt
@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    data = json.loads(request.body)
    event.title = data.get('title')
    event.start_date = data.get('start_date')
    event.end_date = data.get('end_date')
    event.location = data.get('location')
    event.description = data.get('description')
    event.save()
    return JsonResponse({'success': True})

@require_http_methods(["POST"])
@csrf_exempt
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    event.delete()
    return JsonResponse({'success': True})

# Отправка сообщения
@login_required
def inbox(request):
    user_messages = Message.objects.filter(receiver=request.user, is_archived=False)
    archived_messages = Message.objects.filter(receiver=request.user, is_archived=True)
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'users/inbox.html', {'messages': user_messages, 'archived_messages': archived_messages, 'sent_messages': sent_messages})


@login_required
def send_messages(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'users/send_message.html', {'form': form, 'receiver': receiver})


@login_required
def archive_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_archived = True
    message.save()
    messages.success(request, 'Message archived successfully.')
    return redirect('inbox')

@login_required
def unarchive_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_archived = False
    message.save()
    messages.success(request, 'Message unarchived successfully.')
    return redirect('inbox')

@login_required
def users_list(request):
    users = User.objects.exclude(id=request.user.id)  # Исключаем текущего пользователя
    return render(request, 'users/users_list.html', {'users': users})


@login_required
def add_rating(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        emoji = request.POST.get('emoji')
        if emoji:
            rating, created = Rating.objects.get_or_create(post=post, user=request.user, emoji=emoji)
            if not created:
                rating.delete()  # Удаляем существующий рейтинг, если он уже есть
            return redirect('home')
    return redirect('home')