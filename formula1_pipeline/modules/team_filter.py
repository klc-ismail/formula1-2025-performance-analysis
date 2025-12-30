import pandas as pd

#Target teams
TARGET_TEAMS = {
    "RedBull",
    "Ferrari",
    "Mercedes",
    "McLaren",
    "AstonMartin",
}


def normalize_team(team_name: str) -> str:

    if team_name is None:
        return ""

    t = team_name.upper().replace(" ", "")

    if "REDBULL" in t:
        return "RedBull"
    if "FERRARI" in t:
        return "Ferrari"
    if "MERCEDES" in t:
        return "Mercedes"
    if "MCLAREN" in t:
        return "McLaren"
    if "ASTON" in t:
        return "AstonMartin"

    return ""  


def format_driver_filename(driver_number: int, driver_name: str, team_clean: str) -> str:
    clean_name = (driver_name or "").strip().replace(" ", "_")
    clean_team = team_clean.replace(" ", "")
    return f"{driver_number}_{clean_name}_{clean_team}.json"


def filter_drivers_by_team(drivers_df: pd.DataFrame) -> pd.DataFrame:
    
    if drivers_df is None or drivers_df.empty:
        return pd.DataFrame()

    rows = []
    for _, row in drivers_df.iterrows():
        raw_team = row.get("team_name")
        team_clean = normalize_team(raw_team)
        if team_clean and team_clean in TARGET_TEAMS:
            r = row.copy()
            r["team_clean"] = team_clean
            driver_number = int(r["driver_number"])
            driver_name = r.get("broadcast_name") or f"Driver_{driver_number}"
            r["driver_filename"] = format_driver_filename(driver_number, driver_name, team_clean)
            rows.append(r)

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows).reset_index(drop=True)
