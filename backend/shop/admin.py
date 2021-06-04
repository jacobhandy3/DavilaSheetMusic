from django.contrib import admin
from .models import *

#describe model to admin interface
class SheetMusicAdmin(admin.ModelAdmin):
    #list_display lists all the fields in the model
    list_display = ("publisher","title","instrument","ensemble","format","level","genre","description","cost","visible","slug","fpath")
    prepopulated_fields = {"slug": ("title",)}

class ProductResourceAdmin(admin.ModelAdmin):
    list_display = ("product","name","link")
# Register your models here.
admin.site.register(SheetMusic, SheetMusicAdmin)
admin.site.register(ProductResources, ProductResourceAdmin)