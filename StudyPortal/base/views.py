from django.shortcuts import render, redirect
from .models import Note
from .forms import *
from django.contrib import messages
import requests
import wikipedia
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from youtubesearchpython import VideosSearch
# Create your views here.


def index(request):
    return render(request, 'base/home.html')


def login(request):
    if request.method == "POST":
        username_l = request.POST.get('username')
        password_l = request.POST.get('password')
        user = authenticate(request, username=username_l, password=password_l)
        if user is not None:
            auth_login(request, user)
            print('hey')
            return redirect('index')
        else:
            print('bye')
            return redirect('login')
    else:
        form = LoginUser()
        context = {'form': form}
        return render(request, 'base/login.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistraion(request.POST)
        if form.is_valid():
            password1 = request.POST['password1']
            print(password1)
            password2 = request.POST['password2']
            print(password2)
            if password1 == password2:
                print('hyyy')
                form.save()
                print('hyy2')
                print('success')
                print('hyy3')
                return redirect('login')

            else:
                messages.error(
                    request, 'please input correct password in both fields')
                print('unsuccess')
                print('vye')
                return redirect('register')
    else:
        form = UserRegistraion()
        context = {'form': form}
        return render(request, 'base/register.html', context)


def profile(request):
    homework = Homework.objects.filter(user=request.user)
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_s = True
    else:
        todo_s = False

    if len(homework) == 0:
        homework_s = True
    else:
        homework_s = False
    context = {'homework':homework,'todo':todo,'todo_s':todo_s,'homework_s':homework_s}
    return render(request, 'base/profile.html', context)


def logout(request):
    auth_logout(request)
    return redirect('index')


def notes(request):
    form_s = NotesForm()
    note_s = Note.objects.filter(user=request.user)
    if request.method == "POST":
        form_s = NotesForm(request.POST)
        if form_s.is_valid():
            notes = Note(
                user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(
                request, f'Note added succesfully from {request.user.username} user')
    context = {'notes': note_s, 'form': form_s}
    return render(request, 'base/notes.html', context)


def note_delete(request, pk):
    Note.objects.get(id=pk).delete()
    messages.success(request, f"Note deleted succesfully")
    return redirect('notes')


def NotesDetailView(request, pk):
    note_detail = Note.objects.get(id=pk)
    context = {'notes': note_detail}
    return render(request, 'base/notes_detail.html', context)


def homework(request):
    if request.method == "POST":
        form_s = HomeworkForm(request.POST)
        if form_s.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework_s = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished)
            homework_s.save()
            messages.success(
                request, f'Homework added succesfully from {request.user.username} user')
    else:
        form_s = HomeworkForm()
    homework_s = Homework.objects.filter(user=request.user)
    if len(homework_s) == 0:
        homework_s_done = True
    else:
        homework_s_done = False
    context = {'homeworks': homework_s, 'forms': form_s,
               'homework_done': homework_s_done}
    return render(request, 'base/homework.html', context)


def homework_update(request, pk=None):
    homeowrk = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homeowrk.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    messages.success(request, f'Your homework submitted sucessfully')
    return redirect('homework')


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    messages.success(request, f'Your homework deleted sucessfully')
    return redirect('homework')


def youtube_display(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=20)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        context = {'result': result_list, 'forms': form}
        return render(request, 'base/youtube.html', context)
    else:
        form_s = DashboardForm()
    context = {'forms': form_s}
    return render(request, 'base/youtube.html', context)


def todo(request):
    todo = Todo.objects.filter(user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = Todo(user=request.user,
                        title=request.POST['title'], is_finished=finished)
            todo.save()
            messages.success(
                request, f'The todo task is submitted successfully')

    form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_s = True
    else:
        todo_s = False
    context = {'todos': todo, 'form': form, 'todo_s': todo_s}
    return render(request, 'base/todo.html', context)


def delete_todo(request, pk):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


def todo_update(request, pk):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True

    todo.save()
    return redirect('todo')


def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
        context = {'results': result_list, 'forms': form}
        return render(request, 'base/books.html', context)
    else:
        form = DashboardForm()
    form = DashboardForm()
    context = {'form': form}
    return render(request, 'base/books.html', context)


def dictionary(request):

    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        print(text)
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            defination = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonmys']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                # 'audio':audio,
                'defination': defination,
                'example': example,
                'synonyms': synonyms
            }

        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'base/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'base/dictionary.html', context)


def wikipedia_s(request):
    if request.method == "POST":
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'base/wiki.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'base/wiki.html', context)


def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == "lenght":
            form1 = ConversionLengthForm()
            context = {'form': form, 'm_form': form1, 'input': True}
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3}foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form': form,
                    'm_form': form1,
                    'input': True,
                    'answer': answer
                }
        if request.POST['measurement'] == "mass":
            form1 = ConversionMassForm()
            context = {'form': form, 'm_form': form1, 'input': True}
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.2062} pound'
                    print(answer)
                context = {
                    'form': form,
                    'm_form': form1,
                    'input': True,
                    'answer': answer
                }
    else:
        form = ConversionForm()
        context = {'form': form,
                   'input': False}
    return render(request, 'base/conversion.html', context)
