import os
import json
import time
from typing import Any, Dict, Optional

import requests

BASE_URL = "https://api.openf1.org/v1"


def ensure_dir(path: str) -> None:

    os.makedirs(path, exist_ok=True)


def write_json(path: str, data: Any) -> None:

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def safe_slug(text: str) -> str:

    if text is None:
        return "unknown"
    s = text.strip().replace(" ", "_")
    return s


def openf1_get(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    retries: int = 3,
    delay: float = 0.5,
) -> Any:
   
    if params is None:
        params = {}

    url = f"{BASE_URL}/{endpoint}"

    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, params=params, timeout=15)
            if r.status_code == 200:
                return r.json()
            else:
                print(f"{endpoint} ({params}) status={r.status_code}")
        except Exception as e:
            print(f"{endpoint} ({params}) attempt {attempt}/{retries}: {e}")

        time.sleep(delay)

    print(f"Could not fetch {endpoint} with params={params}")
    return None

def normalize_name(text: str) -> str:
    if text is None:
        return "Unknown"

    # Trim + replace whitespace
    s = text.strip().replace(" ", "_")

    clean = "".join(c for c in s if c.isalnum() or c == "_")

    return clean
