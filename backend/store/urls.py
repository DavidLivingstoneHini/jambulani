from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("leagues", views.LeagueViewSet, basename="league")
router.register("collections", views.CollectionViewSet, basename="collection")
router.register("categories", views.CategoryViewSet, basename="category")
router.register("patches", views.PatchViewSet, basename="patch")
router.register("products", views.ProductViewSet, basename="product")
router.register("cart", views.CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
    path("newsletter/subscribe/", views.NewsletterSubscribeView.as_view(), name="newsletter-subscribe"),
]
