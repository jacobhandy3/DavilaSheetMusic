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
        #return filtered objects WHERE objects are public
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
        #return filtered objects WHERE objects are public
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
        queryset = SheetMusic.objects.get(slug=slug)
        return Response({"product": queryset})