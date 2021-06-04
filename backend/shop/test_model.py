from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import *
import json

class SheetMusicTestCase(TestCase):
    def setUp(self):
        testUser = User.objects.create(username='JohnDoe',password='DoeTheMan123')
        SheetMusic.objects.create(
            publisher=testUser,
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            instrument=json.dumps(["Choir","Piano Accompaniment"]),
            ensemble=json.dumps(["4-Part","Mixed Choir","SATB"]),
            format="Score",
            level=3,
            genre="Contemporary Christian Sheet Music",
            description="Test Description",
            cost=24.99,
            visible=True,
        )
        SheetMusic.objects.create(
            publisher=testUser,
            title="ii. la llorona (leyendas del valle)",
            instrument=json.dumps(["Acoustic Guitar","Classical Guitar"]),
            format="Score and parts",
            level=3,
            genre="Classical Sheet Music",
            description="Test Description",
            cost=5.99,
            visible=False,
        )
    def test_get_absolute_url(self):
        """
        Test that checks the url generated off the slug looks the way I need it
        """
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            format="Score",
            level=3,
        )
        # This will also fail if the urlconf is not defined.
        self.assertEqual(testSheet.get_absolute_url(), ('/shop/' + str(testSheet.slug)))
    def test_pub_or_prive(self):
        """
        Test that confirms custom method uses visible attribute to determine whether an instance
        is public or private
        """
        testSheetPub = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            format="Score",
            level=3,
        )
        testSheetPriv = SheetMusic.objects.get(
            title="ii. la llorona (leyendas del valle)",
            format="Score and parts",
            level=3,
        )
        self.assertEqual(testSheetPub.pub_or_priv(),'Public')
        self.assertEqual(testSheetPriv.pub_or_priv(), 'Private')
    def test_list_levels(self):
        """Test that I can retrieve the full list of levels if needed"""
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            format="Score",
            level=3,
        )
        levels = [(1,"Beginner"),(2,"Intermediate"),(3,"Advanced")]
        self.assertEqual(testSheet.listLevels(),levels)
    def test_describe_level(self):
        """
        Tests custom method where the 2nd item in the tuple corresponding to an integer is displayed
        with the describeLevel() method
        """
        testSheet1 = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            format="Score",
            level=3,
        )
        testSheet2 = SheetMusic.objects.get(
            title="ii. la llorona (leyendas del valle)",
            format="Score and parts",
            level=3,
        )
        self.assertEqual(testSheet1.describeLevel(),"Advanced")
        self.assertEqual(testSheet2.describeLevel(), "Advanced")
    def test_slug_created(self):
        """Test that slug is created like I think its going to be created"""
        title_slug = "songs-from-the-book-of-revelation-cantata-for-satb-choir-and-piano-accompaniment"
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            format="Score",
            level=3,
        )
        self.assertEqual(testSheet.slug,title_slug)
    def test_min_val_validate(self):
        """Tests that you cannot set an item at a negative value"""
        testUser = User.objects.get(username='JohnDoe')
        sm = SheetMusic(
            publisher=testUser,
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            instrument=json.dumps(["Choir","Piano Accompaniment"]),
            ensemble=json.dumps(["4-Part","Mixed Choir","SATB"]),
            format="Score",
            level=3,
            genre="Contemporary Christian Sheet Music",
            description="Test Description",
            cost=-5,
            visible=True,
        )
        try:
            sm.full_clean()
        except ValidationError as e:
            self.assertEqual("Cannot input cost amount lower than $0!",e.messages[0])

class ProductResourcesTestCase(TestCase):
    def setUp(self):
        testUser = User.objects.create(username='JohnDoe',password='DoeTheMan123')
        SheetMusic.objects.create(
            publisher=testUser,
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            instrument=json.dumps(["Choir","Piano Accompaniment"]),
            ensemble=json.dumps(["4-Part","Mixed Choir","SATB"]),
            format="Score",
            level=3,
            genre="Contemporary Christian Sheet Music",
            description="Test Description",
            cost=24.99,
            visible=True,
        )
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            format="Score",
            level=3,
        )
        ProductResources.objects.create(
            product=testSheet,
            name="Test Resource",
            link="https://www.sheetmusicplus.com/title/songs-from-the-book-of-revelation-cantata-for-satb-choir-and-piano-accompaniment-digital-sheet-music/22012422"
        )
    def test_resource_created(self):
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            format="Score",
            level=3,
        )
        testResource = ProductResources.objects.get(product=testSheet,name="Test Resource")
        self.assertEqual(testResource.link,"https://www.sheetmusicplus.com/title/songs-from-the-book-of-revelation-cantata-for-satb-choir-and-piano-accompaniment-digital-sheet-music/22012422")