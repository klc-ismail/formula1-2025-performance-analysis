import os
from typing import Any

from .utils import ensure_dir, write_json, safe_slug


def session_dir(year: int, session_key: int, circuit_short_name: str) -> str:
    #Returns the folder path for the relevant race.
    circuit_slug = safe_slug(circuit_short_name)
    base = os.path.join("raw_data", str(year), f"{session_key}_{circuit_slug}")
    ensure_dir(base)
    return base


def session_file_path(year: int, session_key: int, circuit_short_name: str, filename: str) -> str:
    #Returns the session-level file path.
    base = session_dir(year, session_key, circuit_short_name)
    return os.path.join(base, filename)


def driver_file_path(year: int, session_key: int, circuit_short_name: str, driver_filename: str) -> str:
    #Returns the driver-specific file path.
    base = session_dir(year, session_key, circuit_short_name)
    return os.path.join(base, driver_filename)


def save_session_json(year: int, session_key: int, circuit_short_name: str, filename: str, data: Any) -> None:
    #Saves the session-level JSON file.
    path = session_file_path(year, session_key, circuit_short_name, filename)
    write_json(path, data)


def save_driver_json(year: int, session_key: int, circuit_short_name: str, driver_filename: str, data: Any) -> None:
    #It saves a driver-specific JSON file.
    path = driver_file_path(year, session_key, circuit_short_name, driver_filename)
    write_json(path, data)


def session_file_exists(year: int, session_key: int, circuit_short_name: str, filename: str) -> bool:
    #Is there a session-level file?
    path = session_file_path(year, session_key, circuit_short_name, filename)
    return os.path.exists(path)


def driver_file_exists(year: int, session_key: int, circuit_short_name: str, driver_filename: str) -> bool:
    #Is there a driver-specific file?
    path = driver_file_path(year, session_key, circuit_short_name, driver_filename)
    return os.path.exists(path)
