from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),

    # User register login and profile urls
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.profile, name="profile"),

    # Notes page urls
    path('detail-note/<str:pk>', views.NotesDetailView, name="detail-note"),
    path('delete-note/<str:pk>', views.note_delete, name="delete-note"),
    path('notes/', views.notes, name="notes"),

    # Homework page urls
    path('homework/', views.homework, name="homework"),
    path('delete-homework/<str:pk>', views.delete_homework, name="delete-homework"),
    path('homework-update/<str:pk>', views.homework_update, name="homework-update"),

    # Youtube page urls
    path('youtube_videos/', views.youtube_display, name="youtube-display"),

    # Todo page urls
    path('todo/', views.todo, name="todo"),
    path('delete-todo/<str:pk>', views.delete_todo, name="delete-todo"),
    path('todo-update/<str:pk>', views.todo_update, name="todo-update"),

    # Book page urls
    path('books/', views.books, name="books"),

    # Dictionary page urls
    path('dictionary/', views.dictionary, name="dictionary"),

    # wikipidia page urls
    path('wiki/', views.wikipedia_s, name="wikipedia"),

    # conversion page urls
    path('converion/', views.conversion, name="conversion"),
]
