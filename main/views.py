from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.files.base import ContentFile
from django.db.models import Q, Count, QuerySet
from django.forms import modelformset_factory
from django.utils.datastructures import MultiValueDict
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, AddPropertyGoogleForm, LoginUserForm, PropertyImagesForm
from .models import AddPropertyGoogle, User, PropertyImages


class HomePageView(TemplateView):
    template_name = 'main/main.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'term' in request.GET:
            # по введенному в поиск значению берем данные по городам и почтовым кодам
            w = all(i.isdigit() for i in request.GET['term'])
            qs = AddPropertyGoogle.objects.filter(Q(city__icontains=request.GET.get('term'))
                                     | Q(postal_code__icontains=request.GET.get('term')))
            # если в поиске почтовый код
            if w:
                names_code = list(set([f'{i.postal_code}' for i in qs]))
                return JsonResponse(names_code, safe=False)
            # если в поиске город
            names_city = list(set([f'{i.city}, {i.state}' for i in qs]))
            return JsonResponse(names_city, safe=False)
        return self.render_to_response(context)

def raw_sql_search_result_potal_code(query):
    return """SELECT DISTINCT property_id as id, property_id, image, city
                                             FROM main_propertyimages
                                             JOIN main_addpropertygoogle on main_addpropertygoogle.id = main_propertyimages.property_id
                                             where postal_code = %s
                                             GROUP by 1
                                             ORDER by time_update desc""", [query]

def raw_sql_search_result_city(query):
    return """SELECT DISTINCT property_id as id, property_id, image, city
                                             FROM main_propertyimages
                                             JOIN main_addpropertygoogle on main_addpropertygoogle.id = main_propertyimages.property_id
                                             where city = %s
                                             GROUP by 1
                                             ORDER by time_update desc""", [query]
class SearchResultsView(ListView):
    # paginate_by = 2
    def get_template_names(self):
        if self.request.GET.get('q') == '':
            # для пустого значения выводим главную страницу
            return ['main/main.html']
        return ['main/ads_list_exmpl.html']

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        # если почтовый код
        if all(i.isdigit() for i in query):
            # по почтовому коду берем все объявления и их фото, выводим только уникальные варианты объявлений с одним фото
            # objlst1 = PropertyImages.objects.filter(property__postal_code=query).order_by('-property__time_update').distinct('property_id')
            objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_potal_code(int(query)))
            return objlst1
        # если город
        if any(i.isalpha() for i in query):
            # object_list = AddPropertyGoogle.objects.filter(Q(city__icontains=query.split(',')[0])).order_by('-time_update')
            objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_city(query.split(',')[0]))
            return objlst1


# class AddPropertyGoogleView(LoginRequiredMixin, CreateView):
#     form_class = AddPropertyGoogleForm
#     template_name = 'main/add_property_google_multiple_step_form.html'
#     login_url = reverse_lazy("login")
#     success_url = reverse_lazy('add-property')
#
#     def get(self, request, *args, **kwargs):
#         if len(list(request.GET.values())) != 0:
#             return AddPropertyGoogleView.post(self, request)
#         return super().get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         lst_model = ['csrfmiddlewaretoken', 'location', 'apartment_unit',
#                     'property_type', 'city', 'state', 'postal_code', 'country', ]
#         r_post = [v for k, v in request.GET.items()]
#         r_post_new = dict(zip(lst_model, r_post))
#
#
#         a = request.GET.getlist('images')
#         mdict = MultiValueDict({'images': a})
#         bound_form = self.form_class(r_post_new, request.FILES)
#         # bound_form.save()
#         for f in mdict:
#             photo = PropertyImages(property=bound_form, image=f)
#             # photo.property_id = new_obj.id
#             photo.user_id = request.user.id
#             # photo.image.save(f.name, ContentFile(data), True)
#             photo.save()
#
#         # form.instance.user_id = request.user.id
#         if bound_form.is_valid():
#             bound_form.save()
#             return super().form_valid(bound_form)
#         else:
#             return redirect('add-property')

class AddPropertyGoogleView(LoginRequiredMixin, CreateView):
    form_class = AddPropertyGoogleForm
    template_name = 'main/test_form_addproperty.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('add-property')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        lst_model = ['csrfmiddlewaretoken', 'location', 'apartment_unit',
                    'property_type', 'city', 'state', 'postal_code', 'country', ]
        r_post = [v for k, v in request.POST.items()]
        r_post_new = dict(zip(lst_model, r_post))
        bound_form = self.form_class(r_post_new, request.FILES)
        # bound_form.instance.user_id = request.user.id
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.user_id = request.user.id
            new_obj = bound_form.save()
            for f in request.FILES.getlist('images'):
                # data = f.read()  # Если файл целиком умещается в памяти
                photo = PropertyImages(property=new_obj, image=f)
                # photo.property_id = new_obj.id
                photo.user_id = request.user.id
                # photo.image.save(f.name, ContentFile(data), True)
                photo.save()
            return redirect('index')
        return render(request, self.template_name, context={'form': bound_form})

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