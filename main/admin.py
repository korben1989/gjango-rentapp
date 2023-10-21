from django.contrib import admin

from .models import Property, User, PropertyImages, PropertyAddress


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_update', 'user', 'id', 'slug')
    prepopulated_fields = {'slug': ['title']}

class PropertyAddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'neighborhood', 'area', 'city',
                    'state', 'postcode', 'id', 'slug')
    prepopulated_fields = {'slug': ['address', 'neighborhood', 'area', 'city', 'state', 'postcode']}

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class PropertyImagesAdmin(admin.ModelAdmin):
    list_display = ['images', 'property_id']


admin.site.register(Property, PropertyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PropertyImages, PropertyImagesAdmin)
admin.site.register(PropertyAddress, PropertyAddressAdmin)