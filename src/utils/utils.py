from faker import Faker
import random

fake = Faker()

EMAIL_PROVIDERS = ["gmail.com", "yahoo.com", "hotmail.com"]

def generate_email():
    name = fake.user_name() + str(random.randint(100, 9999))
    provider = random.choice(EMAIL_PROVIDERS)
    return f"{name}@{provider}"

def generate_username():
    return fake.user_name() + str(random.randint(10, 9999))

def generate_password():
    return fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True) 