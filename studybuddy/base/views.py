from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
from .forms import RoomForm,UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topic = Topic.objects.all()[0:4]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    context = {'rooms': rooms, 'topics': topic,
               'rooms_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {"room": room, 'room_messages': room_messages,
               'participant': participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='loginPage')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),

        )
        return redirect('index')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/create-room.html', context)


@login_required(login_url='loginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!!')
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('index')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/create-room.html', context)


@login_required(login_url='loginPage')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!!')
    if request.method == "POST":
        room.delete()
        return redirect('index')
    context = {'room': room}
    return render(request, 'base/deleteRoom.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'user doesnot exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username OR Password does not correct')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect('index')


def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user == message.user:
        message.delete()
        return redirect('index')
    else:
        return HttpResponse("You are not allowed to delete the message...")

    return render(request, 'base/home.html')


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    rooms_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': rooms_message, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='loginPage')
def updateUser(request):
    user = request.user
    userForm = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid:
            form.save()
            return redirect('profile',pk=user.id)
    context = {'userForm':userForm}
    return render(request,'base/update-user.html',context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request,'base/topics.html',context)


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request,'base/activity.html',context)