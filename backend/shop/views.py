from django.shortcuts import render, get_object_or_404
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

    def get(self, request):
        #return filtered objects WHERE objects are public and original
        original_filter = self.request.query_params.get('original')
        genre_filter = self.request.query_params.get('genre')
        instrument_filter = self.request.query_params.get('instrument')
        format_filter = self.request.query_params.get('format')
        queryset = SheetMusic.objects.filter(visible=True)
        if original_filter is not None:
            queryset = queryset.filter(original=original_filter)
        if genre_filter is not None:
            genre = get_object_or_404(Genre,slug=genre_filter)
            queryset = queryset.filter(genre__slug=genre.slug)
        if instrument_filter is not None:
            instrument = get_object_or_404(Instrument,slug=instrument_filter)
            queryset = queryset.filter(instrument__slug=instrument.slug)
        if format_filter is not None:
            _format = get_object_or_404(Format,slug=format_filter)
            queryset = queryset.filter(format__slug=_format.slug)
        genres = Genre.objects.all()
        instruments = Instrument.objects.all()
        formats = Format.objects.all()
        return Response({
            "genres":genres,"sheetmusic": queryset,
            "instruments":instruments,"formats":formats,
            })

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
