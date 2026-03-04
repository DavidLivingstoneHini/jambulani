"""
Unit tests for store models.

Covers: discount calculation, slug auto-generation, slug uniqueness,
cart subtotal with and without patches, and model __str__ methods.
"""
from decimal import Decimal

from django.test import TestCase

from store.models import CartItem, Collection, League, Patch, Product



# Helpers
def make_product(**kwargs) -> Product:
    defaults = dict(
        name="Test Shirt",
        price=Decimal("30.00"),
        is_active=True,
        stock=50,
        available_sizes=["S", "M", "L", "XL"],
    )
    defaults.update(kwargs)
    return Product.objects.create(**defaults)



# League
class LeagueModelTest(TestCase):

    def test_str_returns_name(self):
        league = League.objects.create(name="Premier League")
        self.assertEqual(str(league), "Premier League")

    def test_slug_auto_generated_from_name(self):
        league = League.objects.create(name="Champions League")
        self.assertEqual(league.slug, "champions-league")

    def test_existing_slug_not_overwritten_on_resave(self):
        league = League.objects.create(name="La Liga", slug="la-liga-custom")
        league.name = "La Liga Updated"
        league.save()
        self.assertEqual(league.slug, "la-liga-custom")



# Collection
class CollectionModelTest(TestCase):

    def test_str_returns_name(self):
        col = Collection.objects.create(name="Kids Collection")
        self.assertEqual(str(col), "Kids Collection")

    def test_slug_auto_generated(self):
        col = Collection.objects.create(name="Large Sizes")
        self.assertEqual(col.slug, "large-sizes")


# Product
class ProductModelTest(TestCase):

    def setUp(self):
        self.league = League.objects.create(name="Serie A")

    def test_str_returns_name(self):
        p = make_product(name="AC Milan Home Shirt")
        self.assertEqual(str(p), "AC Milan Home Shirt")

    def test_discount_percentage_calculated_correctly(self):
        p = make_product(
            name="AC Milan Home Shirt",
            price=Decimal("30.00"),
            original_price=Decimal("89.95"),
            league=self.league,
        )
        self.assertEqual(p.discount_percentage, 66)

    def test_discount_percentage_is_zero_with_no_original_price(self):
        p = make_product(name="Full Price Shirt", price=Decimal("30.00"))
        self.assertEqual(p.discount_percentage, 0)

    def test_discount_percentage_is_zero_when_prices_are_equal(self):
        p = make_product(
            name="No Discount Shirt",
            price=Decimal("30.00"),
            original_price=Decimal("30.00"),
        )
        self.assertEqual(p.discount_percentage, 0)

    def test_discount_percentage_is_zero_when_price_exceeds_original(self):
        # Guard against negative discounts
        p = make_product(
            name="Weird Shirt",
            price=Decimal("50.00"),
            original_price=Decimal("30.00"),
        )
        self.assertEqual(p.discount_percentage, 0)

    def test_slug_auto_generated_from_name(self):
        p = make_product(name="Real Madrid Home")
        self.assertEqual(p.slug, "real-madrid-home")

    def test_slug_collision_resolved_with_numeric_suffix(self):
        p1 = make_product(name="Barcelona Kit")
        p2 = make_product(name="Barcelona Kit")
        self.assertNotEqual(p1.slug, p2.slug)
        self.assertEqual(p1.slug, "barcelona-kit")
        self.assertEqual(p2.slug, "barcelona-kit-1")

    def test_third_slug_collision_gets_sequential_suffix(self):
        p1 = make_product(name="Bayern Shirt")
        p2 = make_product(name="Bayern Shirt")
        p3 = make_product(name="Bayern Shirt")
        self.assertEqual(p1.slug, "bayern-shirt")
        self.assertEqual(p2.slug, "bayern-shirt-1")
        self.assertEqual(p3.slug, "bayern-shirt-2")

    def test_existing_slug_not_overwritten_on_resave(self):
        p = make_product(name="Juventus Third Kit")
        original_slug = p.slug
        p.name = "Juventus Third Kit Updated"
        p.save()
        self.assertEqual(p.slug, original_slug)


# CartItem subtotal
class CartItemSubtotalTest(TestCase):

    def setUp(self):
        self.product = make_product(
            name="Bayern Munich Home",
            price=Decimal("32.00"),
        )
        self.patch = Patch.objects.create(
            name="Champions League Badge",
            extra_price=Decimal("5.00"),
            is_active=True,
        )

    def test_subtotal_without_patch(self):
        item = CartItem(
            product=self.product,
            size="L",
            quantity=2,
            session_key="test-session-001",
        )
        self.assertEqual(item.subtotal, Decimal("64.00"))

    def test_subtotal_with_patch_adds_extra_price(self):
        item = CartItem(
            product=self.product,
            patch=self.patch,
            size="L",
            quantity=2,
            session_key="test-session-001",
        )
        self.assertEqual(item.subtotal, Decimal("74.00"))

    def test_subtotal_quantity_one(self):
        item = CartItem(
            product=self.product,
            size="M",
            quantity=1,
            session_key="test-session-001",
        )
        self.assertEqual(item.subtotal, Decimal("32.00"))

    def test_subtotal_free_patch_does_not_change_price(self):
        free_patch = Patch.objects.create(
            name="No Patch",
            extra_price=Decimal("0.00"),
            is_active=True,
        )
        item = CartItem(
            product=self.product,
            patch=free_patch,
            size="M",
            quantity=1,
            session_key="test-session-001",
        )
        self.assertEqual(item.subtotal, Decimal("32.00"))
