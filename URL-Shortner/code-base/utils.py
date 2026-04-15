import random
import string

from storage import url_store

def generate_short_url(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))
    # if(temp in url_store):
    #     return generate_short_url(6)