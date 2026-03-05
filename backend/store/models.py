from django.db import models
from django.utils.text import slugify

class League(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    logo = models.ImageField(upload_to="leagues/", blank=True, null=True)
    image = models.ImageField(upload_to="leagues/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'sort_order']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    image = models.ImageField(upload_to="collections/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'sort_order']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children"
    )
    league = models.ForeignKey(
        League, on_delete=models.SET_NULL, null=True, blank=True, related_name="categories"
    )
    collection = models.ForeignKey(
        Collection, on_delete=models.SET_NULL, null=True, blank=True, related_name="categories"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['league', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Patch(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="patches/", blank=True, null=True)
    extra_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "patches"
        indexes = [
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class SizeChart(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="size_charts/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    league = models.ForeignKey(
        League, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    collection = models.ForeignKey(
        Collection, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    available_sizes = models.JSONField(
        default=list,
        help_text='e.g. ["XS","S","M","L","XL","XXL"]',
    )
    patches = models.ManyToManyField(Patch, blank=True)
    size_chart = models.ForeignKey(
        SizeChart, on_delete=models.SET_NULL, null=True, blank=True
    )
    allow_name_customization = models.BooleanField(default=True)
    allow_number_customization = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    stock = models.PositiveIntegerField(default=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['price']),
            models.Index(fields=['league', 'category']),
            models.Index(fields=['created_at']),
            # Composite indexes for common queries
            models.Index(fields=['is_active', 'is_featured', '-created_at']),
            models.Index(fields=['league', 'is_active', 'price']),
            models.Index(fields=['collection', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order"]
        indexes = [
            models.Index(fields=['product', 'is_primary']),
            models.Index(fields=['product', 'sort_order']),
        ]

    def __str__(self):
        return f"{self.product.name} - image {self.sort_order}"


class CartItem(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    custom_name = models.CharField(max_length=100, blank=True)
    custom_number = models.CharField(max_length=2, blank=True)
    patch = models.ForeignKey(Patch, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['session_key', 'created_at']),
            models.Index(fields=['product', 'session_key']),
            models.Index(fields=['session_key', 'product', 'size']),
        ]

    def __str__(self):
        return f"Cart: {self.product.name} x{self.quantity}"

    @property
    def subtotal(self):
        patch_price = self.patch.extra_price if self.patch else 0
        return (self.product.price + patch_price) * self.quantity


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    subscribed_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['subscribed_at']),
        ]

    def __str__(self):
        return self.email
