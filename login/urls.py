from django.contrib import admin
from django.urls import path, re_path

from login import auth_views

urlpatterns = [
    path('', auth_views.IndexView.as_view(), name='login-index'),
    path('async_login/', auth_views.MyLoginView.as_view(), name='login-async_login'),
    path('async_register/', auth_views.MyRegisterView.as_view(), name='login-async_register'),
    re_path('^async_account_confirm/(?P<uidhex>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$', auth_views.MyAccountConfirmView.as_view(), name='login-async_account_confirm'),
    path('async_two_factor_login/', auth_views.TwoFactorAuthentication.as_view(), name='login-async_two_factor'),
    path('async_logout/', auth_views.MyLogoutView.as_view(), name='login-async_logout'),
    path('async_password_reset/', auth_views.MyPasswordResetView.as_view(), name='login-async_reset'),
    path('async_password_reset_done/', auth_views.MyPasswordResetDoneView.as_view(), name='login-async_reset_done'),
    re_path('^async_password_reset/(?P<uidhex>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$', auth_views.MyPasswordResetConfirmView.as_view(), name='login-async_reset_confirm'),
    path('async_password_complete/', auth_views.MyPasswordResetCompleteView.as_view(), name='login-async_reset_complete'),
]
# ]
