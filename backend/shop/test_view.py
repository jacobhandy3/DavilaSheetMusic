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
                title="Sheet Music no. " + str(i),
                format="Score",
                level=(i % 3) + 1,
                genre="Tests",
                description="Test Description...",
                cost=(i ** 3),
                visible=True,
                original=True if i < 5 else False,
            )
    
    def test_view_url_exists_at_desired_location(self):
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        #check original music url is accessible
        response = client.get("/shop/original/")
        self.assertEqual(response.status_code, 200)

        #check arrangement music url is accessible
        response = client.get("/shop/arrangement/")
        self.assertEqual(response.status_code, 200)

        #check individual music url is accessible
        obj = SheetMusic.objects.get(title="Sheet Music no. 1")
        response = client.get("/shop/" + obj.slug)
        self.assertEqual(response.status_code, 200)

    def test_list_urls_accessible_by_name(self):
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        response = client.get(reverse("sheetmusic-list"))
        self.assertEqual(response.status_code, 200)

        response = client.get(reverse("arrangemusic-list"))
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
        self.assertTrue(len(response.data["sheetmusic"]) == 5)
    
    def test_arrangemusic_list(self):
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        response = client.get(reverse("arrangemusic-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["sheetmusic"]) == 5)

    def test_sheetmusic_get(self):
        client = APIClient()
        client.login(username="JohnDoe",password="DoeTheMan123")
        obj = SheetMusic.objects.get(title="Sheet Music no. 1")
        ProductResources.objects.create(product=obj,name="Google test",link="https://www.google.com")
        ProductResources.objects.create(product=obj,name="Yahoo test",link="https://www.yahoo.com")
        resources = ProductResources.objects.filter(product=obj)
        response = client.get(reverse("sheetmusic-detail",args=(obj.slug,)))
        self.assertEqual(response.data["product"],obj)
        self.assertEqual(response.data["links"],resources)