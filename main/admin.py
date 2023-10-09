from django.contrib import admin

from .models import Property, User, PropertyImages


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('time_update', 'user', 'id')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class PropertyImagesAdmin(admin.ModelAdmin):
    list_display = ['images', 'property_id']


admin.site.register(Property, PropertyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PropertyImages, PropertyImagesAdmin)