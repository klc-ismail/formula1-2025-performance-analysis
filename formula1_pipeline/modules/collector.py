import os
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# utils functions
from .utils import openf1_get, write_json, ensure_dir
from .utils import normalize_name  # normalize_name eklenmiş olmalı

# thread limit
MAX_WORKERS = 6


# ============================================================
#   METADATA Download (session-level)
# ============================================================
def download_metadata(session_key: int, session_dir: str):

    print(f"Metadata downloading for session {session_key}...")

    # 1) DRIVERS
    drivers = openf1_get("drivers", {"session_key": session_key})
    if isinstance(drivers, list):
        write_json(os.path.join(session_dir, "drivers.json"), drivers)

    # 2) STARTING GRID
    grid = openf1_get("starting_grid", {"session_key": session_key})
    if isinstance(grid, list):
        write_json(os.path.join(session_dir, "grid.json"), grid)

    # 3) RACE CONTROL (VSC, SC, FLAGS, INCIDENTS)
    rc = openf1_get("race_control", {"session_key": session_key})
    if isinstance(rc, list):
        write_json(os.path.join(session_dir, "race_control.json"), rc)

    # 4) SESSION RESULT (classification)
    sr = openf1_get("session_result", {"session_key": session_key})
    if isinstance(sr, list):
        write_json(os.path.join(session_dir, "session_result.json"), sr)

    print(f"Metadata saved → {session_dir}")


# ============================================================
#   SINGLE DRIVE DATA DOWNLOAD
# ============================================================
def download_driver_data(session_key, circuit, year, driver_row):
    driver_no = int(driver_row["driver_number"])
    driver_name = normalize_name(driver_row["broadcast_name"])
    team_clean = normalize_name(driver_row.get("team_clean", "Unknown"))

    filename = f"{driver_no}_{driver_name}_{team_clean}.json"

    session_dir = f"raw_data/{year}/{session_key}_{circuit}"
    ensure_dir(session_dir)

    full_path = os.path.join(session_dir, filename)

    #RESUME: Download the file again if it already exists.
    if os.path.exists(full_path):
        print(f"{driver_name} already exists — skipping.")
        return full_path

    print(f"Downloading {driver_name} ...")

    data = {}
    endpoints = ["laps", "stints", "pit"]

    for ep in endpoints:
        try:
            df = openf1_get(ep, {"session_key": session_key, "driver_number": driver_no})
            if isinstance(df, list):
                data[ep] = df
            else:
                data[ep] = []
        except Exception as e:
            print(f"      ⚠ Error fetching {ep} for {driver_name}: {e}")
            data[ep] = []

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR saving {filename}: {e}")

    print(f"Finished {driver_name}")
    return full_path


# ============================================================
#   DOWNLOAD ALL DRIVERS IN PARALLEL
# ============================================================
def download_drivers_parallel(session_key, circuit, year, drivers_df):
    session_dir = f"raw_data/{year}/{session_key}_{circuit}"
    ensure_dir(session_dir)

    print(f"Starting driver download ({len(drivers_df)} drivers) for {session_key}...")

    # --- metadata download ---
    download_metadata(session_key, session_dir)

    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(download_driver_data, session_key, circuit, year, row)
            for _, row in drivers_df.iterrows()
        ]

        for f in as_completed(futures):
            results.append(f.result())

    print(f"Completed driver download for session {session_key}\n")
    return results
