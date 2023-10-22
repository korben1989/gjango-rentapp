from django.urls import path, re_path, register_converter

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
    path('add-property', views.AddPropertyView.as_view(), name='add-property'),
    path('', views.HomePageView.as_view(), name='index'),
    # path('search', views.SearchResultsView.as_view(), name='search_results'),
    path('search', views.search_results, name='search_results'),
    path('<slug>', views.result_view, name='results_view'),
    path('404', views.SearchResultsView.as_view(), name='404'),

]