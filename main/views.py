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

def result_view(request, slug):
    obj = get_object_or_404(Postcodes, slug=slug)
    obj1 = PropertyAddress.objects.filter(postcode__icontains=obj)
    return render(request, 'main/ad_display_templates/map_container.html', {'obj': obj, 'obj1': obj1})

def search_results(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = None
        location = request.POST.get('location')

        qs_postcode = PropertyAddress.objects.filter(postcode__icontains=location).distinct('postcode')
        if len(qs_postcode) > 0 and len(location) > 0:
            names_code = [{'postcode': i.postcode, 'slug': i.postcodes.slug} for i in qs_postcode if location in i.postcode]
            res = names_code
            return JsonResponse({'data': res})

        qs_city = PropertyAddress.objects.filter(city__icontains=location).distinct('city')
        if len(qs_city) > 0 and len(location) > 0:
            names_city = [{'city': f'{i.city}, {i.state}', 'slug': i.citys.slug} for i in qs_city if
                          location.lower() in i.city.lower()]
            res = names_city
            return JsonResponse({'data': res})

        qs_area = PropertyAddress.objects.filter(area__icontains=location).distinct('area')
        if len(qs_area) > 0 and len(location) > 0:
            names_area = [{'area': f'{i.area}, {i.city}, {i.state}', 'slug': i.areas.slug} for i in qs_area if
                          location.lower() in i.area.lower()]
            res = names_area
            return JsonResponse({'data': res})

        qs_neighborhood = PropertyAddress.objects.filter(neighborhood__icontains=location).distinct('neighborhood')
        if len(qs_neighborhood) > 0 and len(location) > 0:
            names_neighborhood = [{'neighborhood': f'{i.neighborhood}, {i.city}, {i.state}', 'slug': i.neighborhoods.slug}
                                  for i in qs_neighborhood if location.lower() in i.neighborhood.lower()]
            res = names_neighborhood
            return JsonResponse({'data': res})

        qs_address = PropertyAddress.objects.filter(address__icontains=location)
        if len(qs_address) > 0 and len(location) > 0:
            names_address = [{'address': f'{i.address}, {i.area}, {i.city}, {i.state}, {i.postcode}', 'slug': i.slug}
                              if i.area else {'address': f'{i.address}, {i.city}, {i.state}, {i.postcode}', 'slug': i.slug} for i in qs_address if location.lower() in i.address.lower()]
            res = names_address
            return JsonResponse({'data': res})

        else:
            res = 'No results ...'
        return JsonResponse({'data': res})
    return JsonResponse({})

class SearchResultsView(ListView):
    paginate_by = 2

    def get_template_names(self):
        if self.request.GET.get('q') == '':
            # для пустого значения выводим главную страницу
            return ['main/main.html']
        return ['main/ad_display_templates/map_container.html']

    def get_queryset(self):  # новый
        req_name = self.request.GET.get('q')

        query = self.request.GET.get('q').split('-')
        query = [i.strip() for i in query]

        # address
        if len(query) >= 4:
            qs = PropertyAddress.objects.values('property_id').filter(
                Q(address__icontains=query[0]) & Q(city__icontains=query[-3]) &
                Q(state__icontains=query[-2]) & Q(postcode__icontains=query[-1])
            )
            d = [i['property_id'] for i in qs]

            qs1 = Property.objects.filter(id__in=d). \
                prefetch_related(Prefetch('propertyimages_set', to_attr='img')). \
                prefetch_related(Prefetch('propertyinfo_set', to_attr='info')). \
                prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')
            return qs1

        # neighborhood or area
        if len(query) == 3:
            qs = PropertyAddress.objects.values('property_id').filter(
                (Q(neighborhood__icontains=query[0]) | Q(area__icontains=query[0])) &
                Q(city__icontains=query[1]) & Q(state__icontains=query[2])
            )
            d = [i['property_id'] for i in qs]

            qs1 = Property.objects.filter(id__in=d). \
                prefetch_related(Prefetch('propertyimages_set', to_attr='img')). \
                prefetch_related(Prefetch('propertyinfo_set', to_attr='info')). \
                prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')
            return qs1

        # city
        if len(query) == 2:
            # if '?' not in req_name:
            qs = PropertyAddress.objects.values('property_id').filter(
                Q(city__icontains=query[0]) & Q(state__icontains=query[1])
            )
            d = [i['property_id'] for i in qs]

            qs1 = Property.objects.filter(id__in=d).\
                prefetch_related(Prefetch('propertyimages_set', to_attr='img')).\
                prefetch_related(Prefetch('propertyinfo_set', to_attr='info')).\
                prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')
            return qs1
            # else:
            #     req_name = self.request.GET.get('q')
            #     req_name = req_name.split('?')
            #
            #     if len(req_name[0].split(',')) == 2:
            #         qs = PropertyAddress.objects.filter(
            #             Q(city__icontains=req_name[0].split(',')[0])
            #             | Q(state__icontains=req_name[0].split(',')[0])
            #         )
            #         return qs

        # postcode
        if len(query) == 1:
            qs = PropertyAddress.objects.values('property_id').filter(Q(postcode__icontains=query[0]))
            d = [i['property_id'] for i in qs]

            qs1 = Property.objects.filter(id__in=d). \
                prefetch_related(Prefetch('propertyimages_set', to_attr='img')). \
                prefetch_related(Prefetch('propertyinfo_set', to_attr='info')). \
                prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')
            return qs1

        # if '?' not in req_name:
        #     # address
        #     if len(query) >= 4:
        #         dct = {'address': query[0], 'city': query[1], 'state': query[2], 'postcode': query[3],}
        #         objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_address(dct))
        #         return objlst1
        #
        #     # neighborhood or area
        #     if len(query) == 3:
        #         dct = {'neighborhood_area': query[0], 'city': query[1], 'state': query[2]}
        #         objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_neighborhood_area(dct))
        #         return objlst1
        #
        #     # city
        #     if len(query) == 2:
        #         dct = {'city': query[0], 'state': query[1]}
        #         objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_city(dct))
        #         return objlst1
        #
        #     # postcode
        #     if len(query) == 1:
        #         dct = {'postcode': query[0]}
        #         objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_postcode(dct))
        #         return objlst1
        # else:
        #     query = self.request.GET.get('q')
        #     query = query.split('?')
        #     query_location = query[0].split(',')
        #     query_page = query[1]
        #
        #     # query = self.request.GET.get('q').split(',')
        #     query_location = [i.strip() for i in query_location]
        #
        #     if len(query_location) == 2:
        #         dct = {'city': query_location[0], 'state': query_location[0]}
        #         objlst1 = PropertyImages.objects.raw(*raw_sql_search_result_city(dct))
        #         objlst1 = objlst1[0]
        #         return objlst1



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

                if a['neighborhood'] and a['area']:
                    area = Areas.objects.get_or_create(area_name=a['area'].title(), city=city[0], state=state[0])
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
                elif a['neighborhood'] and not a['area']:
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
                elif not a['neighborhood'] and a['area']:
                    area = Areas.objects.get_or_create(area_name=a['area'].title(), city=city[0], state=state[0])
                    postcode = Postcodes.objects.get_or_create(postcode_name=a['postcode'], area=area[0], city=city[0],
                                                               state=state[0])
                elif not a['neighborhood'] and not a['area']:
                    postcode = Postcodes.objects.get_or_create(postcode_name=a['postcode'], city=city[0], state=state[0])

                form_address = form_address.save(commit=False)
                form_address.latitude = a['location'][1:-2].split(',')[0]
                form_address.longitude = a['location'][1:-2].split(',')[1]
                form_address.property_id = new_obj.id
                form_address.city = form_address.city.title()
                if merg:
                    form_address.neighborhood = merg

                # сохраняю и привязываю к основному адресу
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
                raise Http404('This address alredy exist!')

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