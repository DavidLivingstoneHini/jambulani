from rest_framework.throttling import SimpleRateThrottle, AnonRateThrottle
import ipaddress


class BurstRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made in a short burst.

    Used to prevent rapid-fire requests from overwhelming the API.
    """
    scope = 'burst'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class AuthEndpointThrottle(SimpleRateThrottle):
    """
    Strict throttling for authentication endpoints to prevent brute force.
    """
    scope = 'auth'

    def get_cache_key(self, request, view):
        # Use IP address for auth endpoints to prevent distributed attacks
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class IPBasedThrottle(AnonRateThrottle):
    """
    Enhanced anonymous throttling that respects IP ranges and allows
    whitelisting of trusted IPs.
    """
    scope = 'anon'

    def __init__(self):
        self.trusted_networks = [
            ipaddress.ip_network('127.0.0.0/8'),
            ipaddress.ip_network('10.0.0.0/8'),
            ipaddress.ip_network('172.16.0.0/12'),
            ipaddress.ip_network('192.168.0.0/16'),
        ]
        super().__init__()

    def get_cache_key(self, request, view):
        # Get client IP
        client_ip = self.get_ident(request)

        try:
            ip = ipaddress.ip_address(client_ip)

            # Skip throttling for trusted internal networks
            for network in self.trusted_networks:
                if ip in network:
                    return None

        except ValueError:
            # Invalid IP format, still throttle
            pass

        return self.cache_format % {
            'scope': self.scope,
            'ident': client_ip
        }


class CartOperationThrottle(SimpleRateThrottle):
    """
    Specific throttling for cart operations.
    """
    scope = 'cart'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class CheckoutThrottle(SimpleRateThrottle):
    """
    Strict throttling for checkout to prevent abuse.
    """
    scope = 'checkout'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class ProductListThrottle(SimpleRateThrottle):
    """
    Throttling for product listing endpoints.
    """
    scope = 'product_list'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }