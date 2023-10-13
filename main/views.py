from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.db.models import Q
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, PropertyForm, LoginUserForm, PropertyInfoForm, PropertyImagesForm, \
    ProperyAddressForm, PropertyAmenitiesForm, PropertyAddUnitForm
from .models import Property, User, PropertyImages


class HomePageView(TemplateView):
    template_name = 'main/main.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'term' in request.GET:
            # по введенному в поиск значению берем данные по городам и почтовым кодам
            w = all(i.isdigit() for i in request.GET['term'])
            qs = Property.objects.filter(Q(city__icontains=request.GET.get('term'))
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
    return """SELECT DISTINCT main_propertyimages.property_id as id, *
                                             FROM main_propertyimages
                                             JOIN main_addpropertygoogle on main_addpropertygoogle.id = main_propertyimages.property_id
                                             JOIN main_propertyinfo on main_addpropertygoogle.id = main_propertyinfo.property_id
                                             where postal_code = %s
                                             GROUP by 1
                                             ORDER by time_update desc""", [query]

def raw_sql_search_result_city(query):
    return """SELECT DISTINCT property_id as id, property_id, *
                                             FROM main_propertyimages
                                             JOIN main_addpropertygoogle on main_addpropertygoogle.id = main_propertyimages.property_id
                                             JOIN main_propertyinfo on main_addpropertygoogle.id = main_propertyinfo.property_id
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
            # objlst1 = PropertyImages.objects.filter(property__postal_code=query).order_by('-property__time_update').distinct('property_id')
            objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_potal_code(int(query)))
            return objlst1
        # если город
        if any(i.isalpha() for i in query):
            # object_list = AddPropertyGoogle.objects.filter(Q(city__icontains=query.split(',')[0])).order_by('-time_update')
            objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_city(query.split(',')[0]))
            return objlst1


class AddPropertyView(LoginRequiredMixin, CreateView):
    form_class = PropertyForm
    template_name = 'main/add_prop_form/3.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('add-property')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form_address = ProperyAddressForm
        form_info = PropertyInfoForm
        form_image = PropertyImagesForm
        form_amenities = PropertyAmenitiesForm
        form_unit = PropertyAddUnitForm
        return render(request, self.template_name, context={'form': form,
                                                            'form_info': form_info,
                                                            'form_image': form_image,
                                                            'form_address': form_address,
                                                            'form_amenities': form_amenities,
                                                            # 'form_unit': form_unit,
                                                            })

    def post(self, request, *args, **kwargs):
        a = request.POST.copy()
        a1 = request.FILES
        bound_form = self.form_class(a, request.FILES)

        form_address = ProperyAddressForm(a)
        form_address.changed_data.extend(['latitude', 'longitude'])

        form_amenities = PropertyAmenitiesForm(a)
        form_info = PropertyInfoForm(a)
        # form_unit = PropertyAddUnitForm(a, request.FILES)

        if bound_form.is_valid() and form_amenities.is_valid() \
                and form_info.is_valid() and form_address.is_valid() :
            new_obj = bound_form.save(commit=False)
            new_obj.user_id = request.user.id
            new_obj = bound_form.save()

            form_address = form_address.save(commit=False)
            form_address.latitude = a['location'][1:-2].split(',')[0]
            form_address.longitude = a['location'][1:-2].split(',')[1]
            form_address.property_id = new_obj.id
            form_address.save()

            amenities_form = form_amenities.save(commit=False)
            amenities_form.property_id = new_obj.id
            amenities_form.save()

            # unit_form = form_unit.save(commit=False)
            # unit_form.property_id = new_obj.id
            # unit_form.save()

            info_form = form_info.save(commit=False)
            info_form.property_id = new_obj.id
            info_form.save()

            for f in request.FILES.getlist('images'):
                photo = PropertyImages(property=new_obj, images=f)
                photo.user_id = request.user.id
                photo.save()
            return redirect('index')
        return render(request, self.template_name, context={'form': bound_form,
                                                            'form_info': form_info,
                                                            'form_address': form_address,
                                                            'form_amenities': form_amenities,
                                                            # 'form_unit': form_unit,
                                                            })

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