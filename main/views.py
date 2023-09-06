from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.db.models import Q
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, AddPropertyGoogleForm, LoginUserForm
from .models import AddPropertyGoogle, User


# Create your views here.
# def main(request):
#     return render(request, 'main/main.html')


class HomePageView(TemplateView):
    template_name = 'main/main.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'term' in request.GET:
            w = all(i.isdigit() for i in request.GET['term'])
            qs = AddPropertyGoogle.objects.filter(Q(city__icontains=request.GET.get('term'))
                                     | Q(postal_code__icontains=request.GET.get('term')))
            if w:
                names_code = list(set([f'{i.postal_code}' for i in qs]))
                return JsonResponse(names_code, safe=False)
            names_city = list(set([f'{i.city}, {i.state}' for i in qs]))
            return JsonResponse(names_city, safe=False)
        return self.render_to_response(context)


class SearchResultsView(ListView):
    def get_template_names(self):
        if self.request.GET.get('q') == '':
            return ['main/main.html']
        return ['main/ads_list.html']

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        if all(i.isdigit() for i in query):
            object_list = AddPropertyGoogle.objects.filter(
                Q(postal_code__icontains=query)).order_by('-time_update')
            return object_list
        if any(i.isalpha() for i in query):
            object_list = AddPropertyGoogle.objects.filter(
                Q(city__icontains=query.split(',')[0])).order_by('-time_update')
            return object_list


class AddPropertyGoogleView(LoginRequiredMixin, CreateView):
    form_class = AddPropertyGoogleForm
    template_name = 'main/add_property_google_multiple_step_form.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('add-property')


    def post(self, request, *args, **kwargs):
        lst_model = ['location', 'apartment_unit',
                  'property_type', 'city', 'state', 'postal_code', 'country']

        r_post = [v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken']
        r_post_new = dict(zip(lst_model, r_post))
        form = AddPropertyGoogleForm(r_post_new)
        form.instance.user_id = request.user.id

        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return redirect('add-property')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "main/login.html"

    def get_success_url(self):
        return reverse_lazy('index')


def logout_view(request):
    logout(request)
    return redirect('login')


class ResetPass(PasswordResetView):
    template_name = 'main/password_reset_form.html'
    success_url = reverse_lazy('reset_pass_done')

    def form_valid(self, form):
        users = User.objects.all()
        user_mail = [i.email for i in users]
        # user = User.objects.get(email=form.cleaned_data['email'])
        if form.cleaned_data['email'] in user_mail:
            return super().form_valid(form)
        return super().form_invalid(form)

def reset_pass_done(request):
    subject_template_name = 'main/password_reset_done.html'
    return render(request, subject_template_name)

class PassResetConfView(PasswordResetConfirmView):
    template_name = "main/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class PassResetComplView(PasswordResetCompleteView):
    template_name = "main/password_reset_complete.html"