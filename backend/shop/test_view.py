from rest_framework.test import APIClient,APITestCase,RequestsClient
from django.http import response
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import make_aware
from datetime import timedelta,datetime
import json
from .models import *

class SheetMusicTests(APITestCase):
    def setUp(self):
        testUser = User.objects.create(username="JohnDoe",password="DoeTheMan123")
        for i in range(10):
            SheetMusic.objects.create(
                publisher=testUser,
                composer="John Doe",
                title="Sheet Music no. " + str(i),
                level=(i % 5) + 1,
                description="Test Description...",
                cost=(i ** 3),
                visible=True,
                original=True if i < 5 else False,
            )
        Genre.objects.create(name="Pop")
        Genre.objects.create(name="Rock")
        Instrument.objects.create(name="Tuba")
        Instrument.objects.create(name="Choir")
        Format.objects.create(name="SATB")
        Format.objects.create(name="4-Part")
    
    def test_view_url_exists_at_desired_location(self):
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        #check original music url is accessible
        response = client.get("/shop/")
        self.assertEqual(response.status_code, 200)

        #check individual music url is accessible
        obj = SheetMusic.objects.get(title="Sheet Music no. 1")
        response = client.get("/shop/" + obj.slug)
        self.assertEqual(response.status_code, 200)

    def test_list_url_accessible_by_name(self):
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        response = client.get(reverse("sheetmusic-list"))
        self.assertEqual(response.status_code, 200)

    def test_detail_url_accessible_by_name(self):
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        obj = SheetMusic.objects.get(title="Sheet Music no. 1")
        response = client.get(reverse("sheetmusic-detail",args=(obj.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_sheetmusic_list(self):
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        response = client.get(reverse("sheetmusic-list"))
        self.assertEqual(response.status_code, 200)
        """Tests all sheetmusic,genres,instruments, and formats are being sent"""
        self.assertTrue(len(response.data["sheetmusic"]) == 10)
        self.assertTrue(len(response.data["genres"]) == 2)
        self.assertTrue(len(response.data["instruments"]) == 2)
        self.assertTrue(len(response.data["formats"]) == 2)
    
    def test_list_original_queryparam(self):
        """Test that query param returns correctly filtered results"""
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        #dict attached in response represents the query param
        response = client.get("/shop/",{"original":True})
        queryset = SheetMusic.objects.filter(original=True)
        self.assertEqual(len(queryset),len(response.data["sheetmusic"]))

    def test_list_genre_queryparam(self):
        """Test that query param returns correctly filtered results"""
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        #Add the many-to-many fields
        obj1 = SheetMusic.objects.get(title="Sheet Music no. 1")
        obj1.genre.add(Genre.objects.get(slug="pop"))

        obj2 = SheetMusic.objects.get(title="Sheet Music no. 2")
        obj2.genre.add(Genre.objects.get(slug="pop"))
        #dict attached in response represents the query param
        response = client.get("/shop/",{"genre":"pop"})
        # Ex:genre__slug is how you access the slug field of the genre model through the many-to-many field
        queryset = SheetMusic.objects.filter(genre__slug="pop")
        self.assertEqual(len(queryset),len(response.data["sheetmusic"]))

    def test_list_instrument_queryparam(self):
        """Test that query param returns correctly filtered results"""
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        #Add the many-to-many fields
        obj1 = SheetMusic.objects.get(title="Sheet Music no. 1")
        obj1.instrument.add(Instrument.objects.get(slug="tuba"))

        obj2 = SheetMusic.objects.get(title="Sheet Music no. 2")
        obj2.instrument.add(Instrument.objects.get(slug="tuba"))
        #dict attached in response represents the query param
        response = client.get("/shop/",{"instrument":"tuba"})
        # Ex:instrument__slug is how you access the slug field of the instrument model through the many-to-many field
        queryset = SheetMusic.objects.filter(instrument__slug="tuba")
        self.assertEqual(len(queryset),len(response.data["sheetmusic"]))

    def test_list_format_queryparam(self):
        """Test that query param returns correctly filtered results"""
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        #Add the many-to-many fields
        obj1 = SheetMusic.objects.get(title="Sheet Music no. 1")
        obj1.format.add(Format.objects.get(slug="satb"))

        obj2 = SheetMusic.objects.get(title="Sheet Music no. 2")
        obj2.format.add(Format.objects.get(slug="satb"))
        #dict attached in response represents the query param
        response = client.get("/shop/",{"_format":"satb"})
        # Ex:format__slug is how you access the slug field of the format model through the many-to-many field
        queryset = SheetMusic.objects.filter(format__slug="satb")
        self.assertEqual(len(queryset),len(response.data["sheetmusic"]))

    def test_list_mult_queryparams(self):
        """Test that multiple queryparams correctly filters results"""
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        obj1 = SheetMusic.objects.get(title="Sheet Music no. 1")
        obj2 = SheetMusic.objects.get(title="Sheet Music no. 2")
        #Add the many-to-many fields
        obj1.genre.add(Genre.objects.get(slug="pop"))
        obj1.instrument.add(Instrument.objects.get(slug="tuba"))
        obj1.format.add(Format.objects.get(slug="satb"))

        obj2.genre.add(Genre.objects.get(slug="pop"))
        obj2.instrument.add(Instrument.objects.get(slug="tuba"))
        obj2.format.add(Format.objects.get(slug="satb"))
        #dict attached in response represents the query param
        response = client.get("/shop/",{"original":True,"genre":"pop","instrument":"tuba","_format":"satb"})
        # Ex:format__slug is how you access the slug field of the format model through the many-to-many field
        queryset = SheetMusic.objects.filter(original=True,genre__slug="pop",instrument__slug="tuba",format__slug="satb")
        self.assertEqual(len(queryset),len(response.data["sheetmusic"]))

    def test_sheetmusic_get(self):
        """Test that both the product and its links can be sent"""
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        obj = SheetMusic.objects.get(title="Sheet Music no. 1")
        ProductResources.objects.create(product=obj,name="Google test",link="https://www.google.com")
        ProductResources.objects.create(product=obj,name="Yahoo test",link="https://www.yahoo.com")
        resources = ProductResources.objects.filter(product=obj)
        response = client.get(reverse("sheetmusic-detail",args=(obj.slug,)))
        self.assertEqual(response.data["product"],obj)
        self.assertEqual(len(response.data["links"]),len(resources))