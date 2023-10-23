# def get_template_names(self):
#     if self.request.GET.get('q') == '':
#         # для пустого значения выводим главную страницу
#         return ['main/main.html']
#     return ['main/ad_display_templates/map_container.html']
#
#
# def get_queryset(self):  # новый
#     req_name = self.request.GET.get('q')
#
#     query = self.request.GET.get('q').split('-')
#     query = [i.strip() for i in query]
#
#     # address
#     if len(query) >= 4:
#         qs = PropertyAddress.objects.values('property_id').filter(
#             Q(address__icontains=query[0]) & Q(city__icontains=query[-3]) &
#             Q(state__icontains=query[-2]) & Q(postcode__icontains=query[-1])
#         )
#         d = [i['property_id'] for i in qs]
#
#         qs1 = Property.objects.filter(id__in=d). \
#             prefetch_related(Prefetch('propertyimages_set', to_attr='img')). \
#             prefetch_related(Prefetch('propertyinfo_set', to_attr='info')). \
#             prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')
#         return qs1
#
#     # neighborhood or area
#     if len(query) == 3:
#         qs = PropertyAddress.objects.values('property_id').filter(
#             (Q(neighborhood__icontains=query[0]) | Q(area__icontains=query[0])) &
#             Q(city__icontains=query[1]) & Q(state__icontains=query[2])
#         )
#         d = [i['property_id'] for i in qs]
#
#         qs1 = Property.objects.filter(id__in=d). \
#             prefetch_related(Prefetch('propertyimages_set', to_attr='img')). \
#             prefetch_related(Prefetch('propertyinfo_set', to_attr='info')). \
#             prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')
#         return qs1
#
#     # city
#     if len(query) == 2:
#         # if '?' not in req_name:
#         qs = PropertyAddress.objects.values('property_id').filter(
#             Q(city__icontains=query[0]) & Q(state__icontains=query[1])
#         )
#         d = [i['property_id'] for i in qs]
#
    #         qs1 = Property.objects.filter(id__in=d). \
    #             prefetch_related(Prefetch('propertyimages_set', to_attr='img')). \
    #             prefetch_related(Prefetch('propertyinfo_set', to_attr='info')). \
    #             prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')
#         return qs1
#         # else:
#         #     req_name = self.request.GET.get('q')
#         #     req_name = req_name.split('?')
#         #
#         #     if len(req_name[0].split(',')) == 2:
#         #         qs = PropertyAddress.objects.filter(
#         #             Q(city__icontains=req_name[0].split(',')[0])
#         #             | Q(state__icontains=req_name[0].split(',')[0])
#         #         )
#         #         return qs
#
#     # postcode
#     if len(query) == 1:
#         qs = PropertyAddress.objects.values('property_id').filter(Q(postcode__icontains=query[0]))
#         d = [i['property_id'] for i in qs]
#
#         qs1 = Property.objects.filter(id__in=d). \
#             prefetch_related(Prefetch('propertyimages_set', to_attr='img')). \
#             prefetch_related(Prefetch('propertyinfo_set', to_attr='info')). \
#             prefetch_related(Prefetch('propertyaddress_set', to_attr='addr')).order_by('-time_update')
#         return qs1