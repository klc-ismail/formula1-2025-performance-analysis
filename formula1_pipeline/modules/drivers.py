import pandas as pd
from typing import Any, Dict
from .utils import openf1_get


def get_drivers(session_key: int) -> pd.DataFrame:
    
   #Retrieves the driver list for a session from the OpenF1 API. 
   #Returns only the Drivers endpoint.
    
    params: Dict[str, Any] = {"session_key": session_key}
    data = openf1_get("drivers", params=params)

    if not data:
        print(f"⚠ No drivers found for session {session_key}")
        return pd.DataFrame()

    df = pd.DataFrame(data)


    if "driver_number" not in df.columns:
        df["driver_number"] = None
    if "broadcast_name" not in df.columns:
        df["broadcast_name"] = df.get("driver_name", "Unknown")
    if "team_name" not in df.columns:
        df["team_name"] = None

    # clean df
    df = df.sort_values("driver_number").reset_index(drop=True)

    return df
