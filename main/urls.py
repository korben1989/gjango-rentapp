from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from . import views

urlpatterns = [
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('reset_pass', views.ResetPass.as_view(), name='reset_pass'),
    path('reset_pass_done', views.reset_pass_done, name='reset_pass_done'),
    path('confirm/<str:uidb64>/<str:token>', views.PassResetConfView.as_view(),
         name='password_reset_confirm'),
    path('done', views.PassResetComplView.as_view(), name='password_reset_complete'),
    path('search', views.SearchResultsView.as_view(), name='search_results'),
    path('', views.HomePageView.as_view(), name='index'),
    path('add-property', views.AddPropertyGoogleView.as_view(), name='add-property'),
]