import requests
import pandas as pd
import copy

def fetch_race_results(season):
    url = f"https://api.jolpi.ca/ergast/f1/{season}/results/"

    parameters = {
        "limit": 100,
        "offset": 0
    }
    next_page = True
    total = 0
    races_by_key = {}
    try:
        while next_page:
            response = requests.get(url=url, params=parameters)
            response.raise_for_status()
            data = response.json()

            races = data["MRData"]["RaceTable"]["Races"]

            for race in races:
                key = (race["season"], race["round"])

                results = race.get("Results", [])

                if key not in races_by_key:
                    race_copy = copy.deepcopy(race)
                    race_copy["Results"] = []
                    races_by_key[key] = race_copy

                races_by_key[key]["Results"].extend(results)
 

            total = int(data["MRData"].get("total"))

            if parameters["offset"] < total:
                parameters["offset"] += parameters["limit"]
            else:
                next_page = False

        all_races = list(races_by_key.values())

        return all_races
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    

def parse_race_results(races):
    rows = []
    for race in races:
        for result in race["Results"]:
            row = {
                "season": race["season"],
                "round": race["round"],
                "race_name": race["raceName"],
                "race_date": race["date"],
                
                "circuit_id": race["Circuit"]["circuitId"],
                "circuit_name": race["Circuit"]["circuitName"],
                "country": race["Circuit"]["Location"]["country"],
                "locality": race["Circuit"]["Location"]["locality"],

                "driver_id": result["Driver"]["driverId"],
                "driver_code": result["Driver"].get("code"),
                "driver_number": result["Driver"].get("permanentNumber"),
                "driver_first_name": result["Driver"]["givenName"],
                "driver_last_name": result["Driver"]["familyName"],
                "driver_nationality": result["Driver"]["nationality"],
                
                "constructor_id": result.get("Constructor", {}).get("constructorId"),
                "constructor_name": result.get("Constructor", {}).get("name"),
                "constructor_nationality": result.get("Constructor", {}).get("nationality"),

                "grid": result.get("grid"),
                "position": result["position"],
                "position_text": result["positionText"],
                "points": result["points"],
                "laps": result.get("laps"),
                "status": result.get("status"),

                "race_time": result.get("Time", {}).get("time"),
                "race_time_millis": result.get("Time", {}).get("millis"),
                
                "fastest_lap_rank": result.get("FastestLap", {}).get("rank"),
                "fastest_lap_lap": result.get("FastestLap", {}).get("lap"),
                "fastest_lap_time": result.get("FastestLap", {}).get("Time", {}).get("time"),
                "fastest_lap_avg_speed": result.get("FastestLap", {}).get("AverageSpeed", {}).get("speed"),
            }

            rows.append(row)
    
    df = pd.DataFrame(rows)
    return df