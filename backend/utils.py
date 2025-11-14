import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def getenv_bool(key: str, default: bool=False) -> bool:
    return os.getenv(key, str(default)).lower() in {"1","true","yes","y"}

def ensure_url_has_scheme(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
    return url

def build_url(base_url: str, search: str, location:str, date_range:int = 24, start: int = 0) -> str:
    s = search.replace(" ", "+")
    l = location.replace(" ", "+")
    days = 1 if date_range <= 24 else 2 if date_range <= 48 else 3
    return f"{base_url}?q={s}&l={l}&fromage={days}&sort=date&start={start}"

def update_start_param(url: str, start: int) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query["start"] = [str(start)]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))