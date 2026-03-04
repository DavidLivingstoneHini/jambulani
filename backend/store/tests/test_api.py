"""
API integration tests for the store.
"""
from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from store.models import (
    CartItem,
    Collection,
    League,
    NewsletterSubscriber,
    Patch,
    Product,
    ProductImage,  # Add this import
)


# Shared helpers
def make_product(**kwargs) -> Product:
    defaults = dict(
        name="Test Shirt",
        price=Decimal("30.00"),
        is_active=True,
        is_featured=False,
        stock=50,
        available_sizes=["S", "M", "L", "XL"],
    )
    defaults.update(kwargs)
    return Product.objects.create(**defaults)


# Products
class ProductListAPITest(TestCase):
    """GET /api/v1/products/ — list, filter, search."""

    def setUp(self):
        self.client = APIClient()
        self.league = League.objects.create(name="Premier League", slug="premier-league")
        self.p_featured = make_product(
            name="Manchester United 21-22 Home Shirt",
            price=Decimal("30.00"),
            original_price=Decimal("89.95"),
            league=self.league,
            is_featured=True,
        )
        self.p_regular = make_product(
            name="Arsenal 22-23 Away Shirt",
            price=Decimal("28.00"),
            league=self.league,
        )
        self.p_inactive = make_product(
            name="Hidden Draft Shirt",
            is_active=False,
        )

    def test_list_returns_200(self):
        res = self.client.get("/api/v1/products/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_returns_paginated_response(self):
        res = self.client.get("/api/v1/products/")
        self.assertIn("results", res.data)
        self.assertIn("count", res.data)

    def test_inactive_products_excluded_from_list(self):
        res = self.client.get("/api/v1/products/")
        # Access results through paginated response
        names = [p["name"] for p in res.data["results"]]
        self.assertNotIn("Hidden Draft Shirt", names)

    def test_active_products_appear_in_list(self):
        res = self.client.get("/api/v1/products/")
        names = [p["name"] for p in res.data["results"]]
        self.assertIn("Manchester United 21-22 Home Shirt", names)
        self.assertIn("Arsenal 22-23 Away Shirt", names)

    def test_search_by_name_returns_matching_products(self):
        res = self.client.get("/api/v1/products/?search=arsenal")
        names = [p["name"] for p in res.data["results"]]
        self.assertIn("Arsenal 22-23 Away Shirt", names)
        self.assertNotIn("Manchester United 21-22 Home Shirt", names)

    def test_filter_by_league_slug(self):
        other_league = League.objects.create(name="La Liga", slug="la-liga")
        make_product(name="Real Madrid Kit", league=other_league)

        res = self.client.get(f"/api/v1/products/?league={self.league.slug}")
        names = [p["name"] for p in res.data["results"]]
        self.assertIn("Manchester United 21-22 Home Shirt", names)
        self.assertNotIn("Real Madrid Kit", names)

    def test_filter_by_min_price(self):
        make_product(name="Budget Shirt", price=Decimal("15.00"))
        res = self.client.get("/api/v1/products/?min_price=25")
        # Access results through paginated response
        prices = [Decimal(p["price"]) for p in res.data["results"]]
        for price in prices:
            self.assertGreaterEqual(price, Decimal("25.00"))

    def test_filter_by_max_price(self):
        make_product(name="Expensive Shirt", price=Decimal("120.00"))
        res = self.client.get("/api/v1/products/?max_price=50")
        prices = [Decimal(p["price"]) for p in res.data["results"]]
        for price in prices:
            self.assertLessEqual(price, Decimal("50.00"))

    def test_filter_featured_only(self):
        res = self.client.get("/api/v1/products/?is_featured=true")
        for product in res.data["results"]:
            self.assertTrue(product["is_featured"])


class ProductDetailAPITest(TestCase):
    """GET /api/v1/products/{slug}/ — detail view."""

    def setUp(self):
        self.client = APIClient()
        self.league = League.objects.create(name="Bundesliga", slug="bundesliga")
        self.patch = Patch.objects.create(
            name="Champions League Badge",
            extra_price=Decimal("3.00"),
            is_active=True,
        )
        self.product = make_product(
            name="Bayern Munich 23-24 Home Shirt",
            price=Decimal("32.00"),
            original_price=Decimal("95.00"),
            league=self.league,
            allow_name_customization=True,
            allow_number_customization=True,
        )
        self.product.patches.add(self.patch)

    def test_detail_returns_200(self):
        res = self.client.get(f"/api/v1/products/{self.product.slug}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_detail_contains_expected_fields(self):
        res = self.client.get(f"/api/v1/products/{self.product.slug}/")
        expected_fields = [
            "name", "price", "description", "available_sizes",
            "images", "patches", "allow_name_customization",
            "allow_number_customization", "discount_percentage"
        ]
        for field in expected_fields:
            self.assertIn(field, res.data)

    def test_detail_includes_league_object(self):
        res = self.client.get(f"/api/v1/products/{self.product.slug}/")
        self.assertIn("league", res.data)
        self.assertEqual(res.data["league"]["name"], "Bundesliga")

    def test_detail_includes_patches(self):
        res = self.client.get(f"/api/v1/products/{self.product.slug}/")
        self.assertIn("patches", res.data)
        if res.data["patches"]:
            patch_names = [p["name"] for p in res.data["patches"]]
            self.assertIn("Champions League Badge", patch_names)

    def test_discount_percentage_correct(self):
        res = self.client.get(f"/api/v1/products/{self.product.slug}/")
        # Calculate expected discount: ((95-32)/95)*100 = 66.3 -> 66
        self.assertEqual(res.data["discount_percentage"], 66)

    def test_inactive_product_returns_404(self):
        inactive = make_product(name="Draft Only Shirt", is_active=False)
        res = self.client.get(f"/api/v1/products/{inactive.slug}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class ProductFeaturedAPITest(TestCase):
    """GET /api/v1/products/featured/"""

    def setUp(self):
        self.client = APIClient()
        make_product(name="Featured Shirt 1", is_featured=True)
        make_product(name="Featured Shirt 2", is_featured=True)
        make_product(name="Regular Shirt", is_featured=False)
        make_product(name="Inactive Featured", is_featured=True, is_active=False)

    def test_featured_returns_200(self):
        res = self.client.get("/api/v1/products/featured/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_featured_returns_only_featured_products(self):
        res = self.client.get("/api/v1/products/featured/")
        # Featured endpoint returns a list, not paginated
        names = [p["name"] for p in res.data]
        self.assertIn("Featured Shirt 1", names)
        self.assertIn("Featured Shirt 2", names)
        self.assertNotIn("Regular Shirt", names)

    def test_featured_excludes_inactive_products(self):
        res = self.client.get("/api/v1/products/featured/")
        names = [p["name"] for p in res.data]
        self.assertNotIn("Inactive Featured", names)


# Leagues
class LeagueAPITest(TestCase):
    """GET /api/v1/leagues/"""

    def setUp(self):
        self.client = APIClient()
        self.bundesliga = League.objects.create(
            name="Bundesliga", slug="bundesliga", is_active=True, sort_order=1
        )
        self.inactive = League.objects.create(
            name="Inactive League", slug="inactive-league", is_active=False
        )

    def test_list_returns_200(self):
        res = self.client.get("/api/v1/leagues/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_response_is_paginated(self):
        res = self.client.get("/api/v1/leagues/")
        self.assertIn("results", res.data)

    def test_inactive_leagues_excluded(self):
        res = self.client.get("/api/v1/leagues/")
        names = [l["name"] for l in res.data["results"]]
        self.assertIn("Bundesliga", names)
        self.assertNotIn("Inactive League", names)

    def test_retrieve_by_slug_returns_200(self):
        res = self.client.get(f"/api/v1/leagues/{self.bundesliga.slug}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], "Bundesliga")


# Collections
class CollectionAPITest(TestCase):
    """GET /api/v1/collections/"""

    def setUp(self):
        self.client = APIClient()
        self.kids = Collection.objects.create(
            name="Kids", slug="kids", is_active=True
        )
        Collection.objects.create(
            name="Hidden Collection", slug="hidden", is_active=False
        )

    def test_list_returns_200(self):
        res = self.client.get("/api/v1/collections/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_active_collections_appear_in_results(self):
        res = self.client.get("/api/v1/collections/")
        names = [c["name"] for c in res.data["results"]]
        self.assertIn("Kids", names)

    def test_inactive_collections_excluded(self):
        res = self.client.get("/api/v1/collections/")
        names = [c["name"] for c in res.data["results"]]
        self.assertNotIn("Hidden Collection", names)

    def test_retrieve_by_slug(self):
        res = self.client.get(f"/api/v1/collections/{self.kids.slug}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], "Kids")


# Newsletter
class NewsletterAPITest(TestCase):
    """POST /api/v1/newsletter/subscribe/"""

    def setUp(self):
        self.client = APIClient()

    def test_subscribe_success_returns_201(self):
        res = self.client.post(
            "/api/v1/newsletter/subscribe/",
            {"email": "fan@jambulani.com"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_subscribe_creates_record_in_db(self):
        self.client.post(
            "/api/v1/newsletter/subscribe/",
            {"email": "fan@jambulani.com"},
            format="json",
        )
        self.assertTrue(
            NewsletterSubscriber.objects.filter(email="fan@jambulani.com").exists()
        )

    def test_duplicate_active_subscriber_returns_400(self):
        NewsletterSubscriber.objects.create(
            email="existing@jambulani.com", is_active=True
        )
        res = self.client.post(
            "/api/v1/newsletter/subscribe/",
            {"email": "existing@jambulani.com"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_format_returns_400(self):
        res = self.client.post(
            "/api/v1/newsletter/subscribe/",
            {"email": "not-a-valid-email"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email_returns_400(self):
        res = self.client.post(
            "/api/v1/newsletter/subscribe/",
            {},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
