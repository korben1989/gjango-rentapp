from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.db.models import Q, Prefetch
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, PropertyForm, LoginUserForm, PropertyInfoForm, PropertyImagesForm, \
    ProperyAddressForm, PropertyAmenitiesForm, PropertyAddUnitForm
from .models import Property, User, PropertyImages, PropertyAddress, PropertyInfo, Citys, States, Areas, Neighborhoods, \
    Postcodes

from collections import Counter


# живой поиск на главной странице
class HomePageView(TemplateView):
    template_name = 'main/main.html'

# проверка поискового запроса пользователя есть такой объект или нет в модели
def get_or_none(model_or_qs, **kwargs):
    try:
        return get_object_or_404(model_or_qs, **kwargs)
    except Http404:
        return None

def get_search_result(ids):
    return Property.objects.filter(id__in=ids). \
                    prefetch_related(Prefetch('propertyimages_set', to_attr='img')). \
                    prefetch_related(Prefetch('propertyinfo_set', to_attr='info')). \
                    prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')

# выбор пользователем подходящего запроса и отображение страницы поиска
def result_view(request, slug):
    # поиск по моделям запроса пользователя
    obj_postcode = get_or_none(Postcodes, slug=slug)
    obj_city = get_or_none(Citys, slug=slug)
    obj_area = get_or_none(Areas, slug=slug)
    obj_neighborhood = get_or_none(Neighborhoods, slug=slug)
    # если есть соответствие отображаем результат поиска
    for c, i in enumerate([obj_postcode, obj_city, obj_area, obj_neighborhood]):
        if i:
            if c == 0:
                objects_postcode = PropertyAddress.objects.values('property_id').filter(postcode__icontains=i.id)
                ids = [i['property_id'] for i in objects_postcode]
                obj = get_search_result(ids)
                return render(request, 'main/ad_display_templates/map_container.html', {'obj': obj})
            elif c == 1:
                objects_city = PropertyAddress.objects.values('property_id').filter(citys_id=i.id)
                ids = [i['property_id'] for i in objects_city]
                obj = get_search_result(ids)
                return render(request, 'main/ad_display_templates/map_container.html', {'obj': obj})
            elif c == 2:
                objects_area = PropertyAddress.objects.values('property_id').filter(areas_id=i.id)
                ids = [i['property_id'] for i in objects_area]
                obj = get_search_result(ids)
                return render(request, 'main/ad_display_templates/map_container.html', {'obj': obj})
            elif c == 3:
                objects_neighborhood = PropertyAddress.objects.values('property_id').filter(neighborhoods_id=i.id)
                ids = [i['property_id'] for i in objects_neighborhood]
                obj = get_search_result(ids)
                return render(request, 'main/ad_display_templates/map_container.html', {'obj': obj})
    return render(request, 'main/ad_display_templates/map_container.html', {})

# отображение совпадающих результатов поиска пользователю
def search_results(request):
    # если запрос ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = []
        location = request.POST.get('location')
        # собираем все подходящие под запрос данные из таблицы (по горду, району и тд.)
        # и объединяем в один Json список
        qs_postcode = PropertyAddress.objects.filter(postcode__icontains=location).distinct('postcode')
        if len(qs_postcode) > 0 and len(location) > 0:
            names_code = [{'postcode': i.postcode, 'slug': i.postcodes.slug} for i in qs_postcode if location in i.postcode]
            res.extend(names_code)

        qs_city = PropertyAddress.objects.filter(city__icontains=location).distinct('city')
        if len(qs_city) > 0 and len(location) > 0:
            names_city = [{'city': f'{i.city}, {i.state}', 'slug': i.citys.slug} for i in qs_city if
                          location.lower() in i.city.lower()]
            res.extend(names_city)

        qs_area = PropertyAddress.objects.filter(area__icontains=location).distinct('area')
        if len(qs_area) > 0 and len(location) > 0:
            names_area = [{'area': f'{i.area}, {i.city}, {i.state}', 'slug': i.areas.slug} for i in qs_area if
                          location.lower() in i.area.lower()]
            res.extend(names_area)

        qs_neighborhood = PropertyAddress.objects.filter(neighborhood__icontains=location).distinct('neighborhood')
        if len(qs_neighborhood) > 0 and len(location) > 0:
            names_neighborhood = [{'neighborhood': f'{i.neighborhood}, {i.city}, {i.state}', 'slug': i.neighborhoods.slug}
                                  for i in qs_neighborhood if location.lower() in i.neighborhood.lower()]
            res.extend(names_neighborhood)

        qs_address = PropertyAddress.objects.filter(address__icontains=location)
        if len(qs_address) > 0 and len(location) > 0:
            names_address = [{'address': f'{i.address}, {i.area}, {i.city}, {i.state}, {i.postcode}', 'slug': i.slug}
                              if i.area else {'address': f'{i.address}, {i.city}, {i.state}, {i.postcode}', 'slug': i.slug} for i in qs_address if location.lower() in i.address.lower()]
            res.extend(names_address)
        # если есть варианты выводим ограниченное кол-во или ничего если пусто
        if res:
            return JsonResponse({'data': res[:6]})
        else:
            res = 'No result found ...'
        return JsonResponse({'data': res})
    return JsonResponse({})

class SearchResultsView(ListView):
    paginate_by = 2


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

            try:
                # по моделям для штата/города и тд. создаю или беру данные
                st_name, ct_name = a['state'].upper(), a['city'].title()
                state = States.objects.get_or_create(state_name=st_name)
                city = Citys.objects.get_or_create(city_name=ct_name, state=state[0])
                merg = None

                # если есть микрорайон и район
                if a['neighborhood'] and a['area']:
                    area = Areas.objects.get_or_create(area_name=a['area'].title(), city=city[0], state=state[0])
                    # если город входит в название микрорайона, форматируем что бы район был без города
                    if ct_name in a['neighborhood']:
                        merged_lst = a['neighborhood'].split(' ') + ct_name.split(' ')
                        c = Counter(merged_lst)
                        res = [x for x in merged_lst if c[x] == 1 and len(x) > 2]
                        # res = list(filter(lambda x: c[x] == 1, merged_lst))
                        merg = ' '.join(res).title()
                        neighborhood = Neighborhoods.objects.get_or_create(neighborhood_name=merg.title(),
                                                                           area=area[0], city=city[0], state=state[0])
                    else:
                        neighborhood = Neighborhoods.objects.get_or_create(neighborhood_name=a['neighborhood'].title(),
                                                                       area=area[0], city=city[0], state=state[0])
                    postcode = Postcodes.objects.get_or_create(postcode_name=a['postcode'], area=area[0], city=city[0],
                                                               state=state[0])
                # если есть микрорайон и нет района
                elif a['neighborhood'] and not a['area']:
                    # если город входит в название микрорайона, форматируем что бы район был без города
                    if ct_name in a['neighborhood']:
                        merged_lst = a['neighborhood'].split(' ') + ct_name.split(' ')
                        c = Counter(merged_lst)
                        res = [x.strip() for x in merged_lst if c[x] == 1 and len(x) > 2]
                        merg = ' '.join(res).title()
                        neighborhood = Neighborhoods.objects.get_or_create(neighborhood_name=merg.title(),
                                                                           city=city[0], state=state[0])
                    else:
                        neighborhood = Neighborhoods.objects.get_or_create(neighborhood_name=a['neighborhood'].title(),
                                                                           city=city[0], state=state[0])
                    postcode = Postcodes.objects.get_or_create(postcode_name=a['postcode'], city=city[0], state=state[0])
                # если нет микрорайона и есть район
                elif not a['neighborhood'] and a['area']:
                    area = Areas.objects.get_or_create(area_name=a['area'].title(), city=city[0], state=state[0])
                    postcode = Postcodes.objects.get_or_create(postcode_name=a['postcode'], area=area[0], city=city[0],
                                                               state=state[0])
                # если нет микрорайона и нет района
                elif not a['neighborhood'] and not a['area']:
                    postcode = Postcodes.objects.get_or_create(postcode_name=a['postcode'], city=city[0], state=state[0])

                # сохраняем форму, добавляем широту и долготу, добавляем id родителя объявления...
                form_address = form_address.save(commit=False)
                form_address.latitude = a['location'][1:-2].split(',')[0]
                form_address.longitude = a['location'][1:-2].split(',')[1]
                form_address.property_id = new_obj.id
                form_address.city = form_address.city.title()
                form_address.title = form_address.title.title()
                # если есть название района с городом оставляем только район
                if merg:
                    form_address.neighborhood = merg

                # сохраняю и привязываю к основному адресу модели категорий
                form_address.states = state[0]
                form_address.citys = city[0]
                form_address.postcodes = postcode[0]
                if a['area']:
                    form_address.areas = area[0]
                if a['neighborhood']:
                    form_address.neighborhoods = neighborhood[0]
            except:
                raise Http404('Something went wrong!')

            try:
                form_address.save()
            except:
                raise Http404('This address alredy exist! Make the title unique.')

            #добавляем удобства
            amenities_form = form_amenities.save(commit=False)
            amenities_form.property_id = new_obj.id
            amenities_form.save()

            # unit_form = form_unit.save(commit=False)
            # unit_form.property_id = new_obj.id
            # unit_form.save()

            # добавляем информацию
            info_form = form_info.save(commit=False)
            info_form.property_id = new_obj.id
            info_form.save()

            # добавляем изображение
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