from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import *
import json

class SheetMusicTestCase(TestCase):
    def setUp(self):
        testUser = User.objects.create_user(username='JohnDoe',password='DoeTheMan123')
        SheetMusic.objects.create(
            publisher=testUser,
            composer="John Doe",
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
            description="Test Description",
            cost=24.99,
            visible=True,
            original=True,
        )
        SheetMusic.objects.create(
            publisher=testUser,
            composer="John Doe",
            title="ii. la llorona (leyendas del valle)",
            level=3,
            description="Test Description",
            cost=5.99,
            visible=False,
            original=False,
        )
    def test_genre_m_m_ship(self):
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
        )
        testGenre = Genre.objects.create(name="Pop")
        testSheet.genre.add(testGenre)
        # Note:
        #     Ex:genre__slug is how you access the slug field of the genre model through the many-to-many field
        testQueryset = SheetMusic.objects.filter(genre__slug=testGenre.slug)
        self.assertEqual(testQueryset[0],testSheet)
    def test_instrument_m_m_ship(self):
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
        )
        testInstrument = Instrument.objects.create(name="Tuba")
        testSheet.instrument.add(testInstrument)
        # Note:
        #     Ex:instrument__slug is how you access the slug field of the instrument model through the many-to-many field
        testQueryset = SheetMusic.objects.filter(instrument__slug=testInstrument.slug)
        self.assertEqual(testQueryset[0],testSheet)
    def test_format_m_m_ship(self):
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
        )
        testFormat = Format.objects.create(name="SATB")
        testSheet.format.add(testFormat)
        # Note:
        #     Ex:format__slug is how you access the slug field of the format model through the many-to-many field
        testQueryset = SheetMusic.objects.filter(format__slug=testFormat.slug)
        self.assertEqual(testQueryset[0],testSheet)
    def test_get_absolute_url(self):
        """
        Test that checks the url generated off the slug looks the way I need it
        """
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
        )
        # This will also fail if the urlconf is not defined.
        self.assertEqual(testSheet.get_absolute_url(), ('/shop/' + str(testSheet.slug)))
    def test_list_levels(self):
        """Test that I can retrieve the full list of levels if needed"""
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
        )
        levels = [(1,"Beginner"),(2,"Early Intermediate"),(3,"Intermediate"),(4,"Advanced Intermediate"),(5,"Advanced")]
        self.assertEqual(testSheet.listLevels(),levels)
    def test_describe_level(self):
        """
        Tests custom method where the 2nd item in the tuple corresponding to an integer is displayed
        with the describeLevel() method
        """
        testSheet1 = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
        )
        testSheet2 = SheetMusic.objects.get(
            title="ii. la llorona (leyendas del valle)",
            level=3,
        )
        self.assertEqual(testSheet1.describeLevel(),"Intermediate")
        self.assertEqual(testSheet2.describeLevel(), "Intermediate")
    def test_describe_original(self):
        """
        Tests custom method that outputs 'Original' or 'Arrangement' depending on original model field value
        """
        testSheet1 = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
        )
        testSheet2 = SheetMusic.objects.get(
            title="ii. la llorona (leyendas del valle)",
            level=3,
        )
        self.assertEqual(testSheet1.describeOriginal(),"Original")
        self.assertEqual(testSheet2.describeOriginal(), "Arrangement")
    def test_slug_created(self):
        """Test that slug is created like I think its going to be created"""
        title_slug = "songs-from-the-book-of-revelation-cantata-for-satb-choir-and-piano-accompaniment"
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
        )
        self.assertEqual(testSheet.slug,title_slug)
    def test_min_val_validate(self):
        """Tests that you cannot set an item at a negative value"""
        testUser = User.objects.get(username='JohnDoe')
        sm = SheetMusic(
            publisher=testUser,
            composer="John Doe",
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
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
        testUser = User.objects.create_user(username='JohnDoe',password='DoeTheMan123')
        SheetMusic.objects.create(
            publisher=testUser,
            composer="John Doe",
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
            description="Test Description",
            cost=24.99,
            visible=True,
        )
        testSheet = SheetMusic.objects.get(
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
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
            level=3,
        )
        testResource = ProductResources.objects.get(product=testSheet,name="Test Resource")
        self.assertEqual(testResource.link,"https://www.sheetmusicplus.com/title/songs-from-the-book-of-revelation-cantata-for-satb-choir-and-piano-accompaniment-digital-sheet-music/22012422")

class GenreTestCase(TestCase):
    def setUp(self):
        testUser = User.objects.create_user(username='JohnDoe',password='DoeTheMan123')
        Genre.objects.create(name="Pop")
    def test_genre_created(self):
        testGenre = Genre.objects.get(slug="pop")
        self.assertEqual(testGenre.name,"Pop")

class InstrumentTestCase(TestCase):
    def setUp(self):
        testUser = User.objects.create_user(username='JohnDoe',password='DoeTheMan123')
        Instrument.objects.create(name="Tuba")
    def test_genre_created(self):
        testInstrument = Instrument.objects.get(slug="tuba")
        self.assertEqual(testInstrument.name,"Tuba")

class FormatTestCase(TestCase):
    def setUp(self):
        testUser = User.objects.create_user(username='JohnDoe',password='DoeTheMan123')
        Format.objects.create(name="SATB")
    def test_genre_created(self):
        testFormat = Format.objects.get(slug="satb")
        self.assertEqual(testFormat.name,"SATB")