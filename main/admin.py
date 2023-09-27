from django.contrib import admin

from .models import AddPropertyGoogle, User, PropertyImages


class AddPropertyGoogleAdmin(admin.ModelAdmin):
    list_display = ('location', 'apartment_unit',
                  'property_type', 'city', 'state', 'postal_code', 'user', 'time_update')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class PropertyImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'property_id']


admin.site.register(AddPropertyGoogle, AddPropertyGoogleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PropertyImages, PropertyImagesAdmin)