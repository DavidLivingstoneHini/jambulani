"""
API integration tests for the store.

Covers: products (list, filter, search, detail, featured),
leagues, collections, cart (full CRUD + session isolation),
and newsletter subscription.

Key conventions:
- All URLs confirmed against urls.py + DRF router output
- LeagueViewSet / CollectionViewSet use pagination -> access res.data["results"]
- CartViewSet uses /api/v1/cart/ (not /cart/items/) — confirmed from router
- Cart uses session cookies — APIClient carries them automatically
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
        self.league = League.objects.create(name="Premier League")
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
        other_league = League.objects.create(name="La Liga")
        make_product(name="Real Madrid Kit", league=other_league)

        res = self.client.get(f"/api/v1/products/?league={self.league.slug}")
        names = [p["name"] for p in res.data["results"]]
        self.assertIn("Manchester United 21-22 Home Shirt", names)
        self.assertNotIn("Real Madrid Kit", names)

    def test_filter_by_min_price(self):
        make_product(name="Budget Shirt", price=Decimal("15.00"))
        res = self.client.get("/api/v1/products/?min_price=25")
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
        self.league = League.objects.create(name="Bundesliga")
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
        for field in ["name", "price", "description", "available_sizes",
                      "images", "patches", "allow_name_customization",
                      "allow_number_customization", "discount_percentage"]:
            self.assertIn(field, res.data)

    def test_detail_includes_league_object(self):
        res = self.client.get(f"/api/v1/products/{self.product.slug}/")
        self.assertEqual(res.data["league"]["name"], "Bundesliga")
        self.assertEqual(res.data["league"]["slug"], "bundesliga")

    def test_detail_includes_patches(self):
        res = self.client.get(f"/api/v1/products/{self.product.slug}/")
        patch_names = [p["name"] for p in res.data["patches"]]
        self.assertIn("Champions League Badge", patch_names)

    def test_discount_percentage_correct(self):
        res = self.client.get(f"/api/v1/products/{self.product.slug}/")
        self.assertEqual(res.data["discount_percentage"], 66)

    def test_inactive_product_returns_404(self):
        inactive = make_product(name="Draft Only Shirt", is_active=False)
        res = self.client.get(f"/api/v1/products/{inactive.slug}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexistent_slug_returns_404(self):
        res = self.client.get("/api/v1/products/does-not-exist/")
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
        names = [p["name"] for p in res.data]
        self.assertIn("Featured Shirt 1", names)
        self.assertIn("Featured Shirt 2", names)
        self.assertNotIn("Regular Shirt", names)

    def test_featured_excludes_inactive_products(self):
        res = self.client.get("/api/v1/products/featured/")
        names = [p["name"] for p in res.data]
        self.assertNotIn("Inactive Featured", names)

    def test_featured_capped_at_eight_results(self):
        # Create 10 featured products
        for i in range(10):
            make_product(name=f"Extra Featured {i}", is_featured=True)
        res = self.client.get("/api/v1/products/featured/")
        self.assertLessEqual(len(res.data), 8)



# Leagues
class LeagueAPITest(TestCase):
    """
    GET /api/v1/leagues/
    LeagueViewSet uses ReadOnlyModelViewSet -> paginated response.
    Access results via res.data["results"].
    """

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

    def test_retrieve_inactive_league_returns_404(self):
        res = self.client.get(f"/api/v1/leagues/{self.inactive.slug}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)



# Collections
class CollectionAPITest(TestCase):
    """
    GET /api/v1/collections/
    Paginated — access results via res.data["results"].
    """

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


# Cart
class CartAPITest(TestCase):
    """
    Cart is session-based. APIClient carries cookies automatically,
    so session isolation between test methods is handled by setUp
    creating a fresh client each time.

    Router registers /api/v1/cart/
    - POST   /api/v1/cart/           -> add item (create)
    - GET    /api/v1/cart/           -> view cart (list)
    - PATCH  /api/v1/cart/{pk}/      -> update quantity
    - DELETE /api/v1/cart/{pk}/      -> remove item
    - DELETE /api/v1/cart/clear/     -> empty cart
    """

    def setUp(self):
        self.client = APIClient()
        self.product = make_product(
            name="Chelsea 23-24 Home Shirt",
            price=Decimal("33.00"),
            stock=20,
            available_sizes=["S", "M", "L", "XL"],
        )
        self.patch = Patch.objects.create(
            name="Europa League Badge",
            extra_price=Decimal("4.00"),
            is_active=True,
        )

    def _add_item(self, size="M", quantity=1, **kwargs):
        """Helper: add one item and return the response."""
        payload = {
            "product_id": self.product.id,
            "size": size,
            "quantity": quantity,
            **kwargs,
        }
        return self.client.post("/api/v1/cart/", payload, format="json")

    # Empty cart

    def test_empty_cart_returns_200(self):
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_empty_cart_has_no_items(self):
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(res.data["items"], [])
        self.assertEqual(res.data["count"], 0)
        self.assertEqual(Decimal(res.data["total"]), Decimal("0.00"))

    # Add item

    def test_add_item_returns_201(self):
        res = self._add_item()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_add_item_response_contains_id(self):
        res = self._add_item()
        self.assertIn("id", res.data)

    def test_add_item_response_contains_product(self):
        res = self._add_item()
        self.assertEqual(res.data["product"]["name"], "Chelsea 23-24 Home Shirt")

    def test_add_item_appears_in_cart(self):
        self._add_item(size="L", quantity=2)
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["items"][0]["quantity"], 2)

    def test_add_item_with_custom_name_and_number(self):
        res = self._add_item(
            size="M",
            custom_name="LAMPARD",
            custom_number="8",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["custom_name"], "LAMPARD")
        self.assertEqual(res.data["custom_number"], "8")

    def test_add_item_with_patch(self):
        res = self._add_item(patch_id=self.patch.id)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["patch"]["name"], "Europa League Badge")

    def test_subtotal_includes_patch_price(self):
        res = self._add_item(size="M", quantity=2, patch_id=self.patch.id)
        self.assertEqual(Decimal(res.data["subtotal"]), Decimal("74.00"))

    # Duplicate merging

    def test_adding_same_product_and_size_merges_quantity(self):
        self._add_item(size="M", quantity=1)
        self._add_item(size="M", quantity=2)
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["items"][0]["quantity"], 3)

    def test_different_sizes_create_separate_items(self):
        self._add_item(size="S", quantity=1)
        self._add_item(size="XL", quantity=1)
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(res.data["count"], 2)

    # Cart total

    def test_cart_total_is_sum_of_subtotals(self):
        self._add_item(size="M", quantity=2)  # 33.00 × 2 = 66.00
        self._add_item(size="L", quantity=1)  # 33.00 × 1 = 33.00
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(Decimal(res.data["total"]), Decimal("99.00"))

    # Update quantity

    def test_update_quantity_returns_200(self):
        add_res = self._add_item()
        item_id = add_res.data["id"]
        res = self.client.patch(
            f"/api/v1/cart/{item_id}/", {"quantity": 5}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["quantity"], 5)

    def test_update_quantity_to_zero_deletes_item(self):
        add_res = self._add_item()
        item_id = add_res.data["id"]
        res = self.client.patch(
            f"/api/v1/cart/{item_id}/", {"quantity": 0}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(res.data["count"], 0)

    # Delete item

    def test_delete_item_returns_204(self):
        add_res = self._add_item()
        item_id = add_res.data["id"]
        res = self.client.delete(f"/api/v1/cart/{item_id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleted_item_no_longer_in_cart(self):
        add_res = self._add_item()
        item_id = add_res.data["id"]
        self.client.delete(f"/api/v1/cart/{item_id}/")
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(res.data["count"], 0)

    def test_cannot_delete_another_sessions_item(self):
        """Cart items are isolated by session — another client cannot delete them."""
        add_res = self._add_item()
        item_id = add_res.data["id"]
        other_client = APIClient()
        res = other_client.delete(f"/api/v1/cart/{item_id}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # Clear cart

    def test_clear_cart_returns_204(self):
        self._add_item(size="S")
        self._add_item(size="L")
        res = self.client.delete("/api/v1/cart/clear/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_clear_removes_all_items(self):
        self._add_item(size="S")
        self._add_item(size="L")
        self.client.delete("/api/v1/cart/clear/")
        res = self.client.get("/api/v1/cart/")
        self.assertEqual(res.data["count"], 0)

    # Validation
    def test_cannot_add_inactive_product(self):
        inactive = make_product(name="Draft Shirt", is_active=False)
        res = self.client.post("/api/v1/cart/", {
            "product_id": inactive.id,
            "size": "M",
            "quantity": 1,
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_size_returns_400(self):
        res = self.client.post("/api/v1/cart/", {
            "product_id": self.product.id,
            "quantity": 1,
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_product_id_returns_400(self):
        res = self.client.post("/api/v1/cart/", {
            "size": "M",
            "quantity": 1,
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



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
