import random

domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com"]
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]


def get_random_domain(domains):
    return random.choice(domains)


def get_random_name(letters, length):
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_emails(length):
    return get_random_name(letters, length) + '@' + get_random_domain(domains)
