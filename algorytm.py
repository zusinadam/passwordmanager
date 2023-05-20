import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''

    while len(password) < length:
        char = random.choice(characters)
        password += char

    if not is_password_secure(password):
        return generate_password(length)

    return password

def is_password_secure(password):
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)

    return has_lowercase and has_uppercase and has_digit and has_special

# Przykład użycia
password_length = 16
secure_password = generate_password(password_length)
print("Bezpieczne hasło:", secure_password)
