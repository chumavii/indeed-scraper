import os

def getenv_bool(key: str, default: bool=False) -> bool:
    return os.getenv(key, str(default)).lower() in {"1","true","yes","y"}
