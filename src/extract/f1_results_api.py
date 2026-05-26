import requests
import pandas as pd
import copy

def fetch_race_results_by_season(season):
    url = f"https://api.jolpi.ca/ergast/f1/{season}/results/"

    parameters = {
        "limit": 100,
        "offset": 0
    }

    races_by_key = {}

    try:
        while True:
            response = requests.get(url=url, params=parameters)
            response.raise_for_status()
            data = response.json()

            mr_data = data.get("MRData", {})
            total = int(mr_data.get("total", 0))

            races = (
                mr_data
                .get("RaceTable", {})
                .get("Races", [])
            )

            if not races:
                print(
                    f"No races found for season={season}, "
                    f"offset={parameters['offset']}"
                )

            for race in races:
                key = (race.get("season"), race.get("round"))

                results = race.get("Results", [])

                if key not in races_by_key:
                    race_copy = copy.deepcopy(race)
                    race_copy["Results"] = []
                    races_by_key[key] = race_copy

                races_by_key[key]["Results"].extend(results)

            parameters["offset"] += parameters["limit"]

            if parameters["offset"] >= total:
                break

        return list(races_by_key.values())

    except requests.exceptions.RequestException as e:
        print(f"Error fetching season {season}: {e}")
        return []

def fetch_race_results_by_range(start_season, end_season):
    all_races = []

    for season in range(start_season, end_season + 1):
        season_races = fetch_race_results_by_season(season)

        if not season_races:
            print(f"No races found for season {season}")
            continue

        all_races.extend(season_races)

    return all_races

def parse_race_results(races):
    if not races:
        raise ValueError("No races received to parse.")

    rows = []

    for race in races:
        results = race.get("Results", [])

        if not results:
            print(
                f"No results found for season={race.get('season')} "
                f"round={race.get('round')}"
            )
            continue

        for result in results:
            row = {
                "season": race.get("season"),
                "round": race.get("round"),
                "race_name": race.get("raceName"),
                "race_date": race.get("date"),

                "circuit_id": race.get("Circuit", {}).get("circuitId"),
                "circuit_name": race.get("Circuit", {}).get("circuitName"),
                "country": race.get("Circuit", {}).get("Location", {}).get("country"),
                "locality": race.get("Circuit", {}).get("Location", {}).get("locality"),

                "driver_id": result.get("Driver", {}).get("driverId"),
                "driver_code": result.get("Driver", {}).get("code"),
                "driver_number": result.get("Driver", {}).get("permanentNumber"),
                "driver_first_name": result.get("Driver", {}).get("givenName"),
                "driver_last_name": result.get("Driver", {}).get("familyName"),
                "driver_nationality": result.get("Driver", {}).get("nationality"),

                "constructor_id": result.get("Constructor", {}).get("constructorId"),
                "constructor_name": result.get("Constructor", {}).get("name"),
                "constructor_nationality": result.get("Constructor", {}).get("nationality"),

                "grid": result.get("grid"),
                "position": result.get("position"),
                "position_text": result.get("positionText"),
                "points": result.get("points"),
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

    return pd.DataFrame(rows)