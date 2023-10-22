# class HomePageView(TemplateView):
#     template_name = 'main/main.html'

# def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     if 'term' in request.GET:
    #         # по введенному в поиск значению берем данные по городам и почтовым кодам
    #         req = request.GET['term']
    #         qs = PropertyAddress.objects.filter(Q(address__icontains=request.GET.get('term'))
    #                                  | Q(neighborhood__icontains=request.GET.get('term'))
    #                                  | Q(area__icontains=request.GET.get('term'))
    #                                  | Q(city__icontains=request.GET.get('term'))
    #                                  | Q(state__icontains=request.GET.get('term'))
    #                                  | Q(postcode__icontains=request.GET.get('term')))
    #
    #         # если в поиске почтовый код
    #         names_code = list(set([f'{i.postcode}' for i in qs if req in i.postcode]))
    #         if names_code:
    #             return JsonResponse(names_code, safe=False)
    #
    #         # если в поиске город
    #         names_city = list(set([f'{i.city}, {i.state}' for i in qs if req.lower() in i.city.lower()]))
    #         if names_city:
    #             return JsonResponse(names_city, safe=False)
    #
    #         # если в поиске район
    #         names_area = list(set([f'{i.area}, {i.city}, {i.state}' for i in qs if req.lower() in i.area.lower()]))
    #         if names_area:
    #             return JsonResponse(names_area, safe=False)
    #
    #         # если в поиске соседи
    #         names_neighborhood = list(set([f'{i.neighborhood}, {i.city}, {i.state}' for i in qs if req.lower() in i.neighborhood.lower()]))
    #         if names_neighborhood:
    #             return JsonResponse(names_neighborhood, safe=False)
    #
    #         # если в поиске адресс
    #         names_address = list(
    #             set([f'{i.address}, {i.area}, {i.city}, {i.state}, {i.postcode}' for i in qs if req.lower() in i.address.lower()]))
    #         names_address1 = [i.replace(' ,', '').strip() for i in names_address]
    #         if names_address:
    #             return JsonResponse(names_address1, safe=False)
    #
    #     return self.render_to_response(context)