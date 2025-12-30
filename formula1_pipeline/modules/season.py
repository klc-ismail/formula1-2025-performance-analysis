import pandas as pd
from .races import get_races
from .drivers import get_drivers
from .team_filter import filter_drivers_by_team
from .collector import download_drivers_parallel
from .utils import normalize_name


def generate_season_results(year: int = 2025):

    print(f"Starting raw data download for {year} season...\n")

    races = get_races(year)

    total_races = len(races)
    print(f"Found {total_races} race sessions for {year}.\n")

    completed_races = 0

    for _, race in races.iterrows():
        session_key = race["session_key"]
        circuit = normalize_name(race["circuit_short_name"])
        session_name = normalize_name(race.get("session_name", "Race"))

        print(f"Processing session {session_key} - {circuit}")

        # get drivers
        drivers = get_drivers(session_key)
        drivers = filter_drivers_by_team(drivers)

        if drivers.empty:
            print("No target drivers found, skipping.")
            completed_races += 1
            percent = int((completed_races / total_races) * 100)
            print(f"Season progress: {completed_races}/{total_races} ({percent}%)")
            continue

        #DRIVERS ARE DROPPED OFF IN PARALLEL
        download_drivers_parallel(
            session_key=session_key,
            circuit=circuit,
            year=year,
            drivers_df=drivers
        )

        #SEASON PROGRESS %
        completed_races += 1
        percent = int((completed_races / total_races) * 100)
        print(f"Season progress: {completed_races}/{total_races} ({percent}%)")

    print("All races completed.\n")
