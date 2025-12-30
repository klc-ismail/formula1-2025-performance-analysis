import os
import json
import pandas as pd
from pathlib import Path

RAW_ROOT = "raw_data"

laps_rows = []
pits_rows = []
stints_rows = []
summary_rows = []


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def safe_load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


def extract_session_info(session_folder_name):
    """
    10022_Jeddah → (10022, 'Jeddah')
    """
    try:
        parts = session_folder_name.split("_", 1)
        return int(parts[0]), parts[1]
    except:
        return None, session_folder_name


def extract_driver_basic_info(filename):
    """
    1_Max_Verstappen_RedBull.json → (1, 'Max Verstappen')
    """
    base = os.path.basename(filename)

    try:
        driver_number = int(base.split("_")[0])
    except:
        driver_number = None

    name_parts = base.split("_")[1:-1]
    driver_name = " ".join(name_parts).replace(".json", "")

    return driver_number, driver_name


# -------------------------------------------------
# MAIN
# -------------------------------------------------

print("Converting raw_data → master datasets...\n")

for year_dir in Path(RAW_ROOT).glob("*"):
    if not year_dir.is_dir():
        continue

    for session_dir in year_dir.glob("*"):
        if not session_dir.is_dir():
            continue

        session_key, track_name = extract_session_info(session_dir.name)
        if session_key is None:
            continue

        # -------------------------
        # Static session files
        # -------------------------
        grid = safe_load(session_dir / "grid.json")
        results = safe_load(session_dir / "session_result.json")

        # Grid map
        grid_map = {}
        if isinstance(grid, list):
            for g in grid:
                grid_map[g.get("driver_number")] = g.get("position")

        # Result map
        result_map = {}
        if isinstance(results, list):
            for r in results:
                result_map[r.get("driver_number")] = {
                    "position": r.get("position"),
                    "status": r.get("status"),
                    "best_lap_time": r.get("best_lap_time"),
                }

        # -------------------------
        # Driver files
        # -------------------------
        for dj in session_dir.glob("*.json"):

            if dj.name in [
                "grid.json",
                "session_result.json",
                "drivers.json",
                "race_control.json",
            ]:
                continue

            data = safe_load(dj)
            if not isinstance(data, dict):
                continue

            laps = data.get("laps", [])
            stints = data.get("stints", [])
            pits = data.get("pit", [])

            driver_num, driver_name = extract_driver_basic_info(dj.name)
            team_clean = dj.name.split("_")[-1].replace(".json", "")

            # -------------------------
            # DNF FLAG 
            # -------------------------
            res = result_map.get(driver_num, {})
            finish_position = res.get("position")
            dnf_flag = 1 if finish_position is None else 0

            # -------------------------
            # LAPS
            # -------------------------
            for lap in laps:
                laps_rows.append({
                    "session_key": session_key,
                    "track": track_name,
                    "driver": driver_name,
                    "driver_number": driver_num,
                    "lap": lap.get("lap_number"),
                    "s1": lap.get("duration_sector_1"),
                    "s2": lap.get("duration_sector_2"),
                    "s3": lap.get("duration_sector_3"),
                    "lap_time": lap.get("lap_duration"),
                    "pit": lap.get("is_pit_out_lap"),
                    "dnf": dnf_flag,              
                    "team": team_clean,
                })

            # -------------------------
            # PIT STOPS
            # -------------------------
            for p in pits:
                pits_rows.append({
                    "session_key": session_key,
                    "track": track_name,
                    "driver": driver_name,
                    "driver_number": driver_num,
                    "lap": p.get("lap_number"),
                    "pit_duration": p.get("pit_duration"),
                    "team": team_clean,
                })

            # -------------------------
            # STINTS
            # -------------------------
            for s in stints:
                stints_rows.append({
                    "session_key": session_key,
                    "track": track_name,
                    "driver": driver_name,
                    "driver_number": driver_num,
                    "stint": s.get("stint_number"),
                    "compound": s.get("compound"),
                    "lap_start": s.get("lap_start"),
                    "lap_end": s.get("lap_end"),
                    "team": team_clean,
                })

            # -------------------------
            # SUMMARY
            # -------------------------
            summary_rows.append({
                "session_key": session_key,
                "track": track_name,
                "driver": driver_name,
                "driver_number": driver_num,
                "team": team_clean,
                "grid": grid_map.get(driver_num),
                "finish_position": finish_position,
                "status": res.get("status"),
                "best_lap_time": res.get("best_lap_time"),
                "pit_count": len(pits),
                "dnf": dnf_flag,               
            })


# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

print("Saving CSV files...")

pd.DataFrame(laps_rows).to_csv("master_laps.csv", index=False)
pd.DataFrame(pits_rows).to_csv("master_pit.csv", index=False)
pd.DataFrame(stints_rows).to_csv("master_stints.csv", index=False)
pd.DataFrame(summary_rows).to_csv("master_summary.csv", index=False)

print("DONE!")
print("Created:")
print(" - master_laps.csv")
print(" - master_pit.csv")
print(" - master_stints.csv")
print(" - master_summary.csv")
