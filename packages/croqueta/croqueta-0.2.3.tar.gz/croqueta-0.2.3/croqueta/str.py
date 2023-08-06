import random
import string
import hashlib

def hash_string_to_n_digits(s, n = 10):
    """Hash a string to a number with n digits.""" 

    assert n > 0, "Number of digits must be a positive integer"

    # Create a SHA256 hash object
    hasher = hashlib.sha256()

    # Encode the input string and hash it
    hasher.update(s.encode('utf-8'))

    # Convert the hash to an integer
    hash_int = int(hasher.hexdigest(), 16)

    # Scale the hash to the desired number of digits
    hash_scaled = hash_int % (10 ** n)

    return hash_scaled


def generate_random_string(length):
    "Generate a random string of fixed length"
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string