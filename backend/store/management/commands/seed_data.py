from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import League, Collection, Category, Patch, Product


LEAGUES = [
    {"name": "Champions League", "slug": "champions-league", "sort_order": 1},
    {"name": "Europa League", "slug": "europa-league", "sort_order": 2},
    {"name": "Copa America", "slug": "copa-america", "sort_order": 3},
    {"name": "Asian Cup", "slug": "asian-cup", "sort_order": 4},
    {"name": "African Nations Cup", "slug": "african-nations-cup", "sort_order": 5},
    {"name": "England — Premier League", "slug": "england-premier-league", "sort_order": 6},
    {"name": "La Liga", "slug": "la-liga", "sort_order": 7},
    {"name": "Serie A", "slug": "serie-a", "sort_order": 8},
    {"name": "Bundesliga", "slug": "bundesliga", "sort_order": 9},
    {"name": "Ligue 1", "slug": "ligue-1", "sort_order": 10},
]

COLLECTIONS = [
    {"name": "Kids", "slug": "kids", "sort_order": 1},
    {"name": "Large Sizes", "slug": "large-sizes", "sort_order": 2},
    {"name": "Goalkeeper", "slug": "goalkeeper", "sort_order": 3},
    {"name": "Authentic / Pro Player", "slug": "authentic-pro-player", "sort_order": 4},
    {"name": "Shorts", "slug": "shorts", "sort_order": 5},
    {"name": "Socks", "slug": "socks", "sort_order": 6},
]

PATCHES = [
    {"name": "No Patch", "extra_price": 0},
    {"name": "Champions League", "extra_price": 3},
    {"name": "Premier League", "extra_price": 3},
    {"name": "Europa League", "extra_price": 3},
    {"name": "FIFA World Cup", "extra_price": 5},
    {"name": "Copa del Rey", "extra_price": 3},
]

PRODUCTS = [
    # Featured - Premier League
    {
        "name": "Manchester United 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "england-premier-league",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": (
            "The Manchester United 2021-22 home shirt features the iconic red design with "
            "Adidas and Chevrolet branding. This replica shirt is perfect for fans wanting "
            "to show their support in style. Made from recycled materials, this shirt "
            "combines performance with sustainability."
        ),
    },
    {
        "name": "Manchester United 21-22 Away Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "england-premier-league",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": (
            "The Manchester United 2021-22 away shirt in a striking white design. "
            "Show your support wherever you go with this authentic replica kit."
        ),
    },
    {
        "name": "Manchester City 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "england-premier-league",
        "available_sizes": ["S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": (
            "Manchester City's sky blue home shirt for the 2021-22 season. "
            "Worn by the Premier League champions, this replica is a must-have for any City fan."
        ),
    },
    {
        "name": "Liverpool 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "england-premier-league",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": (
            "Liverpool FC's classic red home shirt for 2021-22. "
            "This iconic shirt has been worn at Anfield by some of the greatest players in football history."
        ),
    },
    {
        "name": "Chelsea 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "england-premier-league",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": (
            "Chelsea FC's royal blue home shirt for the 2021-22 season. "
            "A classic design for fans of the Champions League winners."
        ),
    },
    {
        "name": "Arsenal 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "england-premier-league",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": (
            "Arsenal's iconic red and white home shirt for 2021-22. "
            "A must-have for every Gunners fan worldwide."
        ),
    },
    # La Liga
    {
        "name": "Real Madrid 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "la-liga",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": (
            "The iconic Real Madrid home shirt for the 2021-22 season. "
            "Classic all-white design worn by the kings of European football."
        ),
    },
    {
        "name": "FC Barcelona 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "la-liga",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": True,
        "description": (
            "Barcelona's classic blaugrana shirt for 2021-22. "
            "The iconic red and blue stripes that have defined football fashion for over a century."
        ),
    },
    {
        "name": "Atletico Madrid 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "la-liga",
        "available_sizes": ["S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": (
            "Atletico Madrid's distinctive red and white striped shirt for 2021-22. "
            "The shirt of the La Liga champions, featuring the iconic vertical stripes."
        ),
    },
    # Bundesliga
    {
        "name": "Bayern Munich 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "bundesliga",
        "available_sizes": ["S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": (
            "The classic red Bayern Munich shirt for 2021-22. "
            "Germany's most successful club, featuring the iconic Adidas design."
        ),
    },
    {
        "name": "Borussia Dortmund 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "bundesliga",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": (
            "Borussia Dortmund's iconic yellow and black home shirt for 2021-22. "
            "The 'Yellow Wall' shirt worn by the Signal Iduna Park faithful."
        ),
    },
    # Serie A
    {
        "name": "Juventus 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "serie-a",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": (
            "Juventus's iconic black and white striped home shirt for 2021-22. "
            "The Old Lady of Turin's classic design."
        ),
    },
    {
        "name": "AC Milan 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "serie-a",
        "available_sizes": ["S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": (
            "AC Milan's iconic red and black striped home shirt for 2021-22. "
            "The Rossoneri's classic design, worn by champions of Italy and Europe."
        ),
    },
    # Ligue 1
    {
        "name": "PSG 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "ligue-1",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": (
            "Paris Saint-Germain home shirt for the 2021-22 season. "
            "Featuring the iconic Haussmann pattern inspired by the architecture of Paris."
        ),
    },
    # Copa America
    {
        "name": "Argentina 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "copa-america",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": (
            "Argentina's iconic light blue and white striped home shirt. "
            "The shirt worn by the Copa America champions."
        ),
    },
    {
        "name": "Brazil 21-22 Home Shirt",
        "price": 30.00,
        "original_price": 89.95,
        "league_slug": "copa-america",
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "is_featured": False,
        "description": (
            "Brazil's iconic yellow home shirt. "
            "The Canarinho, one of the most recognizable football shirts in the world."
        ),
    },
]


class Command(BaseCommand):
    help = "Seeds the database with initial demo data"

    def handle(self, *args, **options):
        User = get_user_model()

        # Create superuser
        if not User.objects.filter(email="admin@jambulani.com").exists():
            User.objects.create_superuser(email="admin@jambulani.com", password="admin123")
            self.stdout.write(self.style.SUCCESS("Created superuser: admin@jambulani.com / admin123"))

        # Create leagues
        leagues_created = 0
        for data in LEAGUES:
            _, created = League.objects.get_or_create(slug=data["slug"], defaults=data)
            if created:
                leagues_created += 1
        self.stdout.write(f"Leagues: {leagues_created} created, {len(LEAGUES) - leagues_created} already existed")

        # Create collections
        collections_created = 0
        for data in COLLECTIONS:
            _, created = Collection.objects.get_or_create(slug=data["slug"], defaults=data)
            if created:
                collections_created += 1
        self.stdout.write(f"Collections: {collections_created} created, {len(COLLECTIONS) - collections_created} already existed")

        # Create patches
        patches_created = 0
        for data in PATCHES:
            _, created = Patch.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                patches_created += 1
        self.stdout.write(f"Patches: {patches_created} created")

        patches = list(Patch.objects.all())

        # Create products
        products_created = 0
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
                products_created += 1

        self.stdout.write(f"Products: {products_created} created, {len(PRODUCTS) - products_created} already existed")
        self.stdout.write(self.style.SUCCESS("\n✅ Seed complete!"))
        self.stdout.write(f"Featured products: {Product.objects.filter(is_featured=True).count()}")
        self.stdout.write(f"Total products: {Product.objects.count()}")
        self.stdout.write("\nAdmin login: http://localhost:8000/admin")
        self.stdout.write("Email: admin@jambulani.com | Password: admin123")
