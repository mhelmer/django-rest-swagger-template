from django.utils.crypto import get_random_string


def generate_secret_key(filename):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)

    with open(filename, 'w') as f:
        f.write("SECRET_KEY = '" + secret_key + "'")
        f.write("DEBUG = True")
