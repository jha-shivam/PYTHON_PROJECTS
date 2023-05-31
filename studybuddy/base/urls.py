from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='index'),
    path('room/<str:pk>/',views.room,name='room'),
    path('update-room/<str:pk>/',views.updateRoom,name='updateRoom'),
    path('update-user/',views.updateUser,name='updateUser'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='deleteRoom'),
    path('delete-message/<str:pk>/',views.delete_message,name='delete-message'),
    path('create-room/',views.createRoom,name='createRoom'),
    path('login/',views.loginPage,name='loginPage'),
    path('logout/',views.logoutUser,name='logout'),
    path('topics/',views.topicsPage,name='topics'),
    path('activity/',views.activityPage,name='activity'),
    path('profile/<str:pk>/',views.profile,name='profile'),
    path('register/',views.registerPage,name='registerPage'),

]