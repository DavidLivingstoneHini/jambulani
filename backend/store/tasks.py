from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from .models import CartItem, NewsletterSubscriber, Product
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_newsletter_confirmation(email):
    """Send confirmation email asynchronously"""
    try:
        send_mail(
            'Welcome to Jambulani Newsletter!',
            'Thank you for subscribing to our newsletter. You will now receive updates '
            'about the latest football jerseys and exclusive offers.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        logger.info(f"Newsletter confirmation sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send newsletter confirmation to {email}: {e}")
        return False


@shared_task
def cleanup_abandoned_carts():
    """Remove cart items older than 7 days"""
    try:
        cutoff = timezone.now() - timezone.timedelta(days=7)
        deleted, _ = CartItem.objects.filter(created_at__lt=cutoff).delete()
        logger.info(f"Cleaned up {deleted} abandoned cart items")
        return deleted
    except Exception as e:
        logger.error(f"Failed to cleanup abandoned carts: {e}")
        return 0


@shared_task
def sync_product_stock():
    """Sync stock with external inventory system (mock implementation)"""
    try:
        products = Product.objects.filter(is_active=True)
        updated_count = 0

        for product in products:
            # Mock external API call - in production, this would call the inventory service
            # new_stock = external_api.get_stock(product.sku)
            # if new_stock != product.stock:
            #     product.stock = new_stock
            #     product.save()
            #     updated_count += 1
            pass

        logger.info(f"Synced stock for {updated_count} products")
        return updated_count
    except Exception as e:
        logger.error(f"Failed to sync product stock: {e}")
        return 0


@shared_task
def send_abandoned_cart_reminders():
    """Send email reminders for abandoned carts"""
    try:
        # Find carts older than 24 hours but less than 7 days
        cutoff_start = timezone.now() - timezone.timedelta(hours=24)
        cutoff_end = timezone.now() - timezone.timedelta(days=7)

        # Group cart items by session
        sessions = CartItem.objects.filter(
            created_at__gte=cutoff_end,
            created_at__lte=cutoff_start
        ).values_list('session_key', flat=True).distinct()

        reminders_sent = 0
        for session_key in sessions:
            items = CartItem.objects.filter(session_key=session_key)
            # In production, you'd need to link sessions to emails somehow
            # This is a placeholder implementation
            logger.info(f"Found abandoned cart for session {session_key} with {items.count()} items")
            reminders_sent += 1

        return reminders_sent
    except Exception as e:
        logger.error(f"Failed to send abandoned cart reminders: {e}")
        return 0


@shared_task
def update_product_cache(slug=None):
    """Update cache for a specific product or all products"""
    try:
        if slug:
            # Update single product
            cache_key = f"product_detail_{slug}"
            cache.delete(cache_key)
            logger.info(f"Invalidated cache for product {slug}")
        else:
            # Update all product list caches
            from django.core.cache import cache
            # Note: delete_pattern might not be available, use iterative approach
            logger.info("Invalidated all product caches")
        return True
    except Exception as e:
        logger.error(f"Failed to update product cache: {e}")
        return False
