from django.urls import path
from . import views

urlpatterns = [
	
	path('account/', views.AccountUpdate, name='user-account'),
	path('change/password/', views.UserPasswordChangeView.as_view(), name='user-change-password'),
	path('change/password/done/', views.UserPasswordChangeDoneView.as_view(), name='user-change-password-done'),
]