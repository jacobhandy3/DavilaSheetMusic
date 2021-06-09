from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.

class SheetMusicList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "shop/index.html"
    #define serializer_class with custom serializer
    serializer_class = SheetMusicSerializer
    #redefine get_queryset method
    def get_queryset(self):
        return SheetMusic.objects.filter(visible=True,original=True)
    def get(self, request):
        #return filtered objects WHERE objects are public and original
        queryset = SheetMusic.objects.filter(visible=True,original=True)
        return Response({"sheetmusic": queryset})

class ArrangeMusicList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "shop/index.html"
    #define serializer_class with custom serializer
    serializer_class = SheetMusicSerializer
    #redefine get_queryset method
    def get_queryset(self):
        return SheetMusic.objects.filter(visible=True,original=False)
    def get(self, request):
        #return filtered objects WHERE objects are public and arrangements
        queryset = SheetMusic.objects.filter(visible=True,original=False)
        return Response({"sheetmusic": queryset})


#Allows GET, PUT, and DELETE of specific SheetMusic for authenticated users
class SheetMusicDetail(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "shop/product.html"

    #define serializer_class with custom serializer
    serializer_class = SheetMusicSerializer
    lookup_field = "slug"

    def get(self, request, slug):
        #get the object with matching slug
        obj = SheetMusic.objects.get(slug=slug)
        #get list of product resources
        queryset = ProductResources.objects.filter(product=obj)
        """return a dictionary of the product and its links
            iff they exist, otherwise just the object"""
        return Response({"product": obj,"links":queryset}) if queryset.count() > 0 else Response({"product": obj}) 