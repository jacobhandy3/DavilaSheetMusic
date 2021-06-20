from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient,APITestCase
from shop.models import SheetMusic

class SheetMusicTests(APITestCase):
    def setUp(self):
        self.testUser = User.objects.create(username="JohnDoe",password="DoeTheMan123")
        #client to login user
        self.client = APIClient()
        #test Sheet Music object to go into cart
        SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
            description="Test Description",
            cost=24.99,
            visible=True,
            original=True,
        )
        self.testSheet = SheetMusic.objects.get(title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",level=3,)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        #check original music url is accessible
        response = self.client.get("/cart/")
        self.assertEqual(response.status_code, 200)

        #check create cart url is accessible
        response = self.client.get("/cart/create/" + str(self.testSheet.id))
        #redirects to "/cart/"
        self.assertEqual(response.status_code, 302)

        #check delete cart url is accessible
        response = self.client.get("/cart/delete/" + str(self.testSheet.id))
        #redirects to "/cart/"
        self.assertEqual(response.status_code, 302)

    def test_create_url_accessible_by_name(self):
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        response = self.client.get(reverse("cart-create",args=(self.testSheet.id,)))
        #redirects to "/cart/"
        self.assertEqual(response.status_code, 302)

    def test_detail_url_accessible_by_name(self):
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        response = self.client.get(reverse("cart-detail"))
        self.assertEqual(response.status_code, 200)

    def test_delete_url_accessible_by_name(self):
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        response = self.client.get(reverse("cart-delete",args=(self.testSheet.id,)))
        #redirects to "/cart/"
        self.assertEqual(response.status_code, 302)
    
    def test_cart_detail(self):
        """Testing that cart detail view returns a cart object with correct data"""
        product_id = self.testSheet.id
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        #add test sheet to cart
        self.client.post(reverse("cart-create",args=(product_id,)),data={"quantity":1})
        #get the response to cart-detail view to check cart added to render
        response = self.client.get(reverse("cart-detail"))
        #check the costs are the same
        self.assertEqual(response.context["cart"].cart[str(product_id)]["price"],self.testSheet.cost)

    def test_cart_create(self):
        """test that cartCreate view adds items to cart"""
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        #test Sheet Music object to go into cart
        SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="Test Title",
            level=3,
            description="Test Description",
            cost=4.99,
            visible=True,
            original=True,
        )
        temp = SheetMusic.objects.get(title="Test Title")
        #add temp sheet to cart
        self.client.post(reverse("cart-create",args=(temp.id,)),data={"quantity":1})
        #check the costs are the same
        response = self.client.get((reverse("cart-detail")))
        #check the costs are the same
        self.assertEqual(response.context["cart"].cart[str(temp.id)]["price"],temp.cost)

    def test_cart_delete(self):
        """test that cartDelete view removes item from cart"""
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        #test Sheet Music object to go into cart
        SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="RIP",
            level=3,
            description="gg...",
            cost=0.99,
            visible=True,
            original=True,
        )
        """Create a sheet music object to be removed and add it to cart"""
        temp = SheetMusic.objects.get(title="RIP")
        self.client.post(reverse("cart-create",args=(temp.id,)),data={"quantity":1})
        """Check the sheet music object was added to the cart"""
        response = self.client.get((reverse("cart-detail")))
        self.assertEqual(response.context["cart"].cart[str(temp.id)]["price"],temp.cost)
        """Delete the object with cart-delete view and check it doesn't exist anymore"""
        self.client.post(reverse("cart-delete",args=(temp.id,)))
        response = self.client.get((reverse("cart-detail")))
        self.assertIsNone(response.context["cart"].cart.get(str(temp.id)))
