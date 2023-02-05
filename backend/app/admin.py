from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group 


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    search_fields= ('category','type','surface','description','prix')
    list_display= ('user','category','type','surface','prix')
    list_filter= ['category','type']


class ImageAdmin(admin.ModelAdmin):
    search_fields= ('Post','img')
    list_display= ('Post','img')



class WilayaAdmin(admin.ModelAdmin):
    search_fields= ('name',)
    list_display= ('id','name')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class CommuneAdmin(admin.ModelAdmin):
    search_fields= ('name','wilaya__name')
    list_display= ('id','name','wilaya')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class AdressAdmin(admin.ModelAdmin):
    search_fields= ('commune',)
    list_display= ('commune',)

admin.site.register(Post,PostAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Wilaya,WilayaAdmin)
admin.site.register(Commune,CommuneAdmin)
admin.site.register(Adress,AdressAdmin)
admin.site.register(Offre)
admin.site.unregister(Group)