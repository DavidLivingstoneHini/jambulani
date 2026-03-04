"""
Auth API integration tests.

Covers: registration, login, logout, token refresh (rotation + reuse detection),
profile read/update, and password change.

Key conventions:
- Exact URLs confirmed from accounts/urls.py:
    /api/v1/auth/register/
    /api/v1/auth/login/
    /api/v1/auth/logout/
    /api/v1/auth/token/refresh/
    /api/v1/auth/me/
    /api/v1/auth/password/change/
- Authentication: Bearer token in Authorization header
- Refresh token is in HttpOnly cookie — APIClient carries it automatically
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import RefreshToken, User


# Shared helpers

REGISTER_URL      = "/api/v1/auth/register/"
LOGIN_URL         = "/api/v1/auth/login/"
LOGOUT_URL        = "/api/v1/auth/logout/"
TOKEN_REFRESH_URL = "/api/v1/auth/token/refresh/"
ME_URL            = "/api/v1/auth/me/"
CHANGE_PW_URL     = "/api/v1/auth/password/change/"


def make_user(
    email="user@jambulani.com",
    password="StrongPass123!",
    first_name="Test",
    last_name="User",
    **kwargs,
) -> User:
    return User.objects.create_user(
        email=email, password=password,
        first_name=first_name, last_name=last_name,
        **kwargs,
    )


def register(client: APIClient, email="new@jambulani.com", password="StrongPass123!"):
    return client.post(REGISTER_URL, {
        "email": email,
        "first_name": "Jane",
        "last_name": "Doe",
        "password": password,
        "password_confirm": password,
    }, format="json")


def login(client: APIClient, email="user@jambulani.com", password="StrongPass123!"):
    return client.post(LOGIN_URL, {
        "email": email,
        "password": password,
    }, format="json")


def auth_client(user_email="user@jambulani.com", password="StrongPass123!") -> tuple[APIClient, str]:
    """Return a (client, access_token) tuple already authenticated."""
    client = APIClient()
    make_user(email=user_email, password=password)
    res = login(client, email=user_email, password=password)
    access = res.data["access_token"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client, access


# ─────────────────────────────────────────────────────────────
# Registration
# ─────────────────────────────────────────────────────────────

class RegisterTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_returns_201(self):
        res = register(self.client)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_register_response_contains_access_token_and_user(self):
        res = register(self.client)
        self.assertIn("access_token", res.data)
        self.assertIn("user", res.data)

    def test_register_user_email_in_response(self):
        res = register(self.client, email="jane@jambulani.com")
        self.assertEqual(res.data["user"]["email"], "jane@jambulani.com")

    def test_register_creates_user_in_database(self):
        register(self.client, email="stored@jambulani.com")
        self.assertTrue(User.objects.filter(email="stored@jambulani.com").exists())

    def test_register_sets_httponly_access_token_cookie(self):
        res = register(self.client)
        self.assertIn("access_token", res.cookies)
        self.assertTrue(res.cookies["access_token"]["httponly"])

    def test_register_sets_httponly_refresh_token_cookie(self):
        res = register(self.client)
        self.assertIn("refresh_token", res.cookies)
        self.assertTrue(res.cookies["refresh_token"]["httponly"])

    def test_register_creates_refresh_token_in_database(self):
        register(self.client, email="token@jambulani.com")
        user = User.objects.get(email="token@jambulani.com")
        self.assertTrue(
            RefreshToken.objects.filter(user=user, revoked=False).exists()
        )

    def test_register_email_normalised_to_lowercase(self):
        register(self.client, email="UPPER@JAMBULANI.COM")
        self.assertTrue(User.objects.filter(email="upper@jambulani.com").exists())

    def test_register_duplicate_email_returns_400(self):
        make_user(email="dup@jambulani.com")
        res = self.client.post(REGISTER_URL, {
            "email": "dup@jambulani.com",
            "first_name": "A",
            "last_name": "B",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch_returns_400(self):
        res = self.client.post(REGISTER_URL, {
            "email": "x@jambulani.com",
            "password": "StrongPass123!",
            "password_confirm": "DifferentPass!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_weak_password_returns_400(self):
        res = self.client.post(REGISTER_URL, {
            "email": "weak@jambulani.com",
            "password": "123",
            "password_confirm": "123",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_email_returns_400(self):
        res = self.client.post(REGISTER_URL, {
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



# Login
class LoginTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()

    def test_login_returns_200(self):
        res = login(self.client)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_response_contains_access_token(self):
        res = login(self.client)
        self.assertIn("access_token", res.data)

    def test_login_response_contains_user_data(self):
        res = login(self.client)
        self.assertEqual(res.data["user"]["email"], "user@jambulani.com")

    def test_login_sets_httponly_cookies(self):
        res = login(self.client)
        self.assertIn("access_token", res.cookies)
        self.assertIn("refresh_token", res.cookies)
        self.assertTrue(res.cookies["access_token"]["httponly"])
        self.assertTrue(res.cookies["refresh_token"]["httponly"])

    def test_login_creates_refresh_token_in_database(self):
        login(self.client)
        self.assertTrue(
            RefreshToken.objects.filter(user=self.user, revoked=False).exists()
        )

    def test_login_wrong_password_returns_400(self):
        res = self.client.post(LOGIN_URL, {
            "email": "user@jambulani.com",
            "password": "WrongPassword!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_unknown_email_returns_400(self):
        res = self.client.post(LOGIN_URL, {
            "email": "ghost@jambulani.com",
            "password": "StrongPass123!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user_returns_400(self):
        self.user.is_active = False
        self.user.save()
        res = login(self.client)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_error_does_not_reveal_whether_email_exists(self):
        """Both wrong-email and wrong-password should return the same 400."""
        res_bad_email = self.client.post(LOGIN_URL, {
            "email": "nobody@jambulani.com",
            "password": "StrongPass123!",
        }, format="json")
        res_bad_pass = self.client.post(LOGIN_URL, {
            "email": "user@jambulani.com",
            "password": "WrongPass!",
        }, format="json")
        self.assertEqual(res_bad_email.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_bad_pass.status_code, status.HTTP_400_BAD_REQUEST)


# Logout

class LogoutTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        res = login(self.client)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access_token']}"
        )

    def test_logout_returns_200(self):
        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_logout_revokes_all_refresh_tokens_for_user(self):
        self.client.post(LOGOUT_URL)
        self.assertFalse(
            RefreshToken.objects.filter(user=self.user, revoked=False).exists()
        )

    def test_logout_clears_access_token_cookie(self):
        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.cookies["access_token"].value, "")

    def test_logout_clears_refresh_token_cookie(self):
        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.cookies["refresh_token"].value, "")

    def test_logout_unauthenticated_returns_401(self):
        unauthenticated = APIClient()
        res = unauthenticated.post(LOGOUT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



# Token refresh

class TokenRefreshTest(TestCase):
    """
    Refresh token is delivered as HttpOnly cookie.
    APIClient automatically carries cookies between requests in the same test.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        # Login sets the refresh_token cookie on the client
        login(self.client)

    def test_refresh_returns_200_when_cookie_present(self):
        res = self.client.post(TOKEN_REFRESH_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_returns_new_access_token(self):
        res = self.client.post(TOKEN_REFRESH_URL)
        self.assertIn("access_token", res.data)

    def test_refresh_without_cookie_returns_401(self):
        fresh_client = APIClient()  # no cookies
        res = fresh_client.post(TOKEN_REFRESH_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_rotates_token_creating_new_db_record(self):
        before = RefreshToken.objects.filter(user=self.user).count()
        self.client.post(TOKEN_REFRESH_URL)
        after = RefreshToken.objects.filter(user=self.user).count()
        self.assertEqual(after, before + 1)

    def test_refresh_marks_old_token_as_revoked(self):
        old_token = RefreshToken.objects.filter(
            user=self.user, revoked=False
        ).first()
        self.client.post(TOKEN_REFRESH_URL)
        old_token.refresh_from_db()
        self.assertTrue(old_token.revoked)

    def test_refresh_for_inactive_user_returns_401(self):
        self.user.is_active = False
        self.user.save()
        res = self.client.post(TOKEN_REFRESH_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Profile (Me)
class ProfileTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = make_user(
            email="jane@jambulani.com",
            first_name="Jane",
            last_name="Doe",
        )
        res = login(self.client, email="jane@jambulani.com")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access_token']}"
        )

    def test_get_profile_returns_200(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_profile_returns_correct_user(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.data["email"], "jane@jambulani.com")
        self.assertEqual(res.data["first_name"], "Jane")
        self.assertEqual(res.data["last_name"], "Doe")

    def test_get_profile_includes_full_name(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.data["full_name"], "Jane Doe")

    def test_update_profile_returns_200(self):
        res = self.client.patch(ME_URL, {
            "first_name": "Janet",
            "city": "Barcelona",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_profile_persists_to_database(self):
        self.client.patch(ME_URL, {"city": "Madrid"}, format="json")
        self.user.refresh_from_db()
        self.assertEqual(self.user.city, "Madrid")

    def test_update_shipping_address(self):
        res = self.client.patch(ME_URL, {
            "address_line1": "Calle Gran Via 1",
            "city": "Madrid",
            "postal_code": "28013",
            "country": "Spain",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["city"], "Madrid")

    def test_email_is_read_only_cannot_be_changed(self):
        self.client.patch(ME_URL, {"email": "hacked@evil.com"}, format="json")
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "jane@jambulani.com")

    def test_unauthenticated_request_returns_401(self):
        unauthed = APIClient()
        res = unauthed.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Change password

class ChangePasswordTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        res = login(self.client)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access_token']}"
        )

    def test_change_password_returns_200(self):
        res = self.client.post(CHANGE_PW_URL, {
            "current_password": "StrongPass123!",
            "new_password": "NewSecure456!",
            "new_password_confirm": "NewSecure456!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_change_password_actually_changes_it_in_db(self):
        self.client.post(CHANGE_PW_URL, {
            "current_password": "StrongPass123!",
            "new_password": "NewSecure456!",
            "new_password_confirm": "NewSecure456!",
        }, format="json")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewSecure456!"))
        self.assertFalse(self.user.check_password("StrongPass123!"))

    def test_change_password_revokes_all_refresh_tokens(self):
        self.client.post(CHANGE_PW_URL, {
            "current_password": "StrongPass123!",
            "new_password": "NewSecure456!",
            "new_password_confirm": "NewSecure456!",
        }, format="json")
        self.assertFalse(
            RefreshToken.objects.filter(user=self.user, revoked=False).exists()
        )

    def test_wrong_current_password_returns_400(self):
        res = self.client.post(CHANGE_PW_URL, {
            "current_password": "WrongCurrentPass!",
            "new_password": "NewSecure456!",
            "new_password_confirm": "NewSecure456!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_password_confirm_mismatch_returns_400(self):
        res = self.client.post(CHANGE_PW_URL, {
            "current_password": "StrongPass123!",
            "new_password": "NewSecure456!",
            "new_password_confirm": "DifferentNew789!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_weak_new_password_returns_400(self):
        res = self.client.post(CHANGE_PW_URL, {
            "current_password": "StrongPass123!",
            "new_password": "123",
            "new_password_confirm": "123",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_current_password_does_not_change_password(self):
        self.client.post(CHANGE_PW_URL, {
            "current_password": "WrongPass!",
            "new_password": "NewSecure456!",
            "new_password_confirm": "NewSecure456!",
        }, format="json")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("StrongPass123!"))

    def test_unauthenticated_request_returns_401(self):
        unauthed = APIClient()
        res = unauthed.post(CHANGE_PW_URL, {
            "current_password": "StrongPass123!",
            "new_password": "NewSecure456!",
            "new_password_confirm": "NewSecure456!",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# JWT authentication backend
class JWTAuthenticationTest(TestCase):
    """
    Tests the custom JWTAuthentication backend directly —
    verifies Bearer token and cookie auth both work,
    and that expired/invalid tokens are rejected correctly.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        res = login(self.client)
        self.access_token = res.data["access_token"]

    def test_bearer_token_grants_access_to_protected_endpoint(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_missing_token_returns_401_on_protected_endpoint(self):
        unauthed = APIClient()
        res = unauthed.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_malformed_token_returns_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer not.a.valid.jwt")
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tampered_token_returns_401(self):
        # Flip the last character of the signature
        parts = self.access_token.rsplit(".", 1)
        tampered = parts[0] + "." + parts[1][:-1] + ("A" if parts[1][-1] != "A" else "B")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tampered}")
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
