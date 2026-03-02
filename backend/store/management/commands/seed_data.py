from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import League, Collection, Category, Patch, Product


LEAGUES = [
    {"name": "Champions League", "slug": "champions-league"},
    {"name": "Europa League", "slug": "europa-league"},
    {"name": "Copa America", "slug": "copa-america"},
    {"name": "Asian Cup", "slug": "asian-cup"},
    {"name": "African Nations Cup", "slug": "african-nations-cup"},
    {"name": "England — Premier League", "slug": "england-premier-league"},
    {"name": "La Liga", "slug": "la-liga"},
    {"name": "Serie A", "slug": "serie-a"},
    {"name": "Bundesliga", "slug": "bundesliga"},
    {"name": "Ligue 1", "slug": "ligue-1"},
]

COLLECTIONS = [
    {"name": "Kids", "slug": "kids"},
    {"name": "Large Sizes", "slug": "large-sizes"},
    {"name": "Goalkeeper", "slug": "goalkeeper"},
    {"name": "Authentic / Pro Player", "slug": "authentic-pro-player"},
    {"name": "Shorts", "slug": "shorts"},
    {"name": "Socks", "slug": "socks"},
]

PATCHES = [
    {"name": "No Patch", "extra_price": 0},
    {"name": "Champions League", "extra_price": 3},
    {"name": "Premier League", "extra_price": 3},
    {"name": "Europa League", "extra_price": 3},
    {"name": "FIFA World Cup", "extra_price": 5},
]

PRODUCTS = [
    {
        "name": "Manchester United 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "england-premier-league",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": "The Manchester United 2021-22 home shirt features the iconic red design with Adidas and Chevrolet branding. This replica shirt is perfect for fans wanting to show their support in style.",
    },
    {
        "name": "Manchester United 21-22 Away Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "england-premier-league",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": "The Manchester United 2021-22 away shirt in a striking white design. Show your support wherever you go.",
    },
    {
        "name": "Real Madrid 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "la-liga",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": "The iconic Real Madrid home shirt for the 2021-22 season.",
    },
    {
        "name": "FC Barcelona 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "la-liga",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": "Barcelona's classic blaugrana shirt for 2021-22.",
    },
    {
        "name": "Bayern Munich 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "bundesliga",
        "available_sizes": ["S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": "The classic red Bayern Munich shirt for 2021-22.",
    },
    {
        "name": "PSG 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "ligue-1",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": "Paris Saint-Germain home shirt for the 2021-22 season.",
    },
]


class Command(BaseCommand):
    help = "Seeds the database with initial demo data"

    def handle(self, *args, **options):
        User = get_user_model()

        # Create superuser
        if not User.objects.filter(email="admin@jambulani.com").exists():
            User.objects.create_superuser(email="admin@jambulani.com", password="admin123")
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin123"))

        # Create leagues
        for data in LEAGUES:
            league, created = League.objects.get_or_create(slug=data["slug"], defaults=data)
            if created:
                self.stdout.write(f"  Created league: {league.name}")

        # Create collections
        for data in COLLECTIONS:
            collection, created = Collection.objects.get_or_create(slug=data["slug"], defaults=data)
            if created:
                self.stdout.write(f"  Created collection: {collection.name}")

        # Create patches
        for data in PATCHES:
            patch, created = Patch.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                self.stdout.write(f"  Created patch: {patch.name}")

        patches = list(Patch.objects.all())

        # Create products
        for data in PRODUCTS:
            league_slug = data.pop("league_slug")
            league = League.objects.filter(slug=league_slug).first()
            product, created = Product.objects.get_or_create(
                name=data["name"],
                defaults={**data, "league": league},
            )
            if created:
                product.patches.set(patches)
                product.save()
                self.stdout.write(f"  Created product: {product.name}")

        self.stdout.write(self.style.SUCCESS("\nSeed complete!"))
        self.stdout.write("Admin login: http://localhost:8000/admin  |  admin / admin123")
