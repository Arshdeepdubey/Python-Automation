import random
import string


def random_string(length=8):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email():
    return f"e2e.{random_string()}@example.com"


def new_registration_user():
    suffix = random_string()
    return {
        "first_name": "Test",
        "last_name": f"User{suffix}",
        "dob": "1990-01-01",
        "country_code": "US",
        "postal_code": "10001",
        "house_number": "123",
        "street": "Main Street",
        "city": "New York",
        "state": "NY",
        "phone": "5551234567",
        "email": f"e2e.{suffix}@example.com",
        "password": f"E2e-{random_string(12)}-9!",
    }
