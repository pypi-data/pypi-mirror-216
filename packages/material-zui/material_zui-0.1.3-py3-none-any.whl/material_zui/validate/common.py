import validators
from base64 import b64decode


def is_valid_url(url) -> bool: return validators.url(url)  # type: ignore


def is_base64(value: str) -> bool:
    try:
        data = value.split(',')[1]
        decoded_img = b64decode(data)
        return bool(decoded_img)
    except:
        return False
