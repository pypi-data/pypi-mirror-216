from unidecode import unidecode


def standardize(text):
    return unidecode(text)
