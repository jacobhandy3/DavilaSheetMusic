from backend.exportCSV import export_to_csv
from django.contrib import admin
from .models import *

#describe model to admin interface
class SheetMusicAdmin(admin.ModelAdmin):
    #list_display lists all the fields in the model
    list_display = ("publisher","title","level","description","cost","visible","slug","fpath")
    filter_horizontal = ("instrument","format","genre",)
    prepopulated_fields = {"slug": ("title",)}
    #extra actions for the model
    actions = [export_to_csv]

class ProductResourceAdmin(admin.ModelAdmin):
    list_display = ("product","name","link")

class GenreAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    prepopulated_fields = {"slug": ("name",)}

class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    prepopulated_fields = {"slug": ("name",)}

class FormatAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    prepopulated_fields = {"slug": ("name",)}

# Register your models here.
admin.site.register(SheetMusic, SheetMusicAdmin)
admin.site.register(ProductResources, ProductResourceAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Format, FormatAdmin)