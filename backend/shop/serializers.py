from rest_framework import serializers
from .models import *

#serializer for model  for JSON conversion for the frontend
class SheetMusicSerializer(serializers.ModelSerializer):
    #dont allow client to accidently create an instance under a different user
    publisher = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        #define target model
        model = SheetMusic
        #list fields
        fields = ("publisher","title","instrument","ensemble","format","level","genre","description","cost","visible","slug","fpath")
        extra_kwargs = {
            "url":{"view_name":"sheetmusic-detail","lookup_field":"slug"}
        }

class ProductResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        #define target model
        model = ProductResources
        #list fields
        fields = ("product","name","link")

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        #define target model
        model = Genre
        #list fields
        fields = ("name","slug")
        extra_kwargs = {
            "url":{"view_name":"genre-detail","lookup_field":"slug"}
        }

class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        #define target model
        model = Instrument
        #list fields
        fields = ("name","slug")
        extra_kwargs = {
            "url":{"view_name":"instrument-detail","lookup_field":"slug"}
        }

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        #define target model
        model = Format
        #list fields
        fields = ("name","slug")
        extra_kwargs = {
            "url":{"view_name":"format-detail","lookup_field":"slug"}
        }