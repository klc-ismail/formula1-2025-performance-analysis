import pandas as pd
from typing import Any, Dict
from .utils import openf1_get


def get_races(year: int) -> pd.DataFrame:
    """
    It only returns actual Grand Prix races.
    Sprint Race, Sprint Shootout, FP and Qualifying sessions are filtered out.
    Filter:
        session_type == "Race"
        AND
        session_name == "Race"
    """

    data = openf1_get("sessions", params={"year": year})
    if not data:
        print(f"No sessions found for {year}.")
        return pd.DataFrame()

    df = pd.DataFrame(data)

    if df.empty:
        print(f"Empty session list for {year}.")
        return df

    # Normalize lower-case string compare
    df["session_type"] = df["session_type"].astype(str).str.lower()
    df["session_name"] = df["session_name"].astype(str).str.lower()

    # ------------------------------------------------------
    # ONLY CHOOSE THE ACTUAL GRAND PRIX RACE.
    # ------------------------------------------------------
    df = df[
        (df["session_type"] == "race") &
        (df["session_name"] == "race")
    ]

    if df.empty:
        print("No real Race sessions found.")
        return df

    #Check for missing columns.
    for col in ["session_key", "circuit_short_name", "date_start"]:
        if col not in df.columns:
            df[col] = None

    # Remove missing data
    df = df.dropna(subset=["session_key", "circuit_short_name", "date_start"])

    # Sort by date
    df["date_start"] = pd.to_datetime(df["date_start"])
    df = df.sort_values("date_start").reset_index(drop=True)

    print(f"Found {len(df)} REAL Grand Prix races for {year}.")
    return df
