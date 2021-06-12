from django.urls import path

from chat import views, api_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='chat-index'),
    path('chat/<int:id>/', views.UserChatView.as_view(), name='chat-user_chat'),
]

# api vies
urlpatterns += [
    path('api/users/', api_views.UserView.as_view(), name='rest_api-users'),
]
