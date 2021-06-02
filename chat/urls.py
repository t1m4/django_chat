from django.urls import path

from chat import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='chat-index'),
]