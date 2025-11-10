import os
from urllib.parse import urlparse

def getenv_bool(key: str, default: bool=False) -> bool:
    return os.getenv(key, str(default)).lower() in {"1","true","yes","y"}

def ensure_url_has_scheme(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
    return url

def build_url(base_url: str, search: str, location:str) -> str:
    s = search.replace(" ", "+")
    l = location.replace(" ", "+")
    return f"{base_url}?q={s}&l={l}"