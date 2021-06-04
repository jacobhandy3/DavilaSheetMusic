from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

# Create your views here.

#Lists all mandatory SheetMusic and user-defined SheetMusic
#Allows creation of SheetMusic as well
class SheetMusicList(generics.ListAPIView):
    #define serializer_class with custom serializer
    serializer_class = SheetMusicSerializer
    #redefine get_queryset method
    def get_queryset(self):
        #return filtered objects WHERE objects are public
        return SheetMusic.objects.filter(visible=True)

#Allows GET, PUT, and DELETE of specific SheetMusic for authenticated users
class SheetMusicDetail(generics.RetrieveAPIView):
    queryset = SheetMusic.objects.all()
    #define serializer_class with custom serializer
    serializer_class = SheetMusicSerializer
    lookup_field = "slug"