import pandas as pd
from src.load.read_from_db import read_from_db_by_query
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)

def create_driver_season_stats():
    query = """
            SELECT
                R.season,
                F.driver_id,
                D.driver_first_name,
                D.driver_last_name,
                F.race_id,
                F.position,
                F.points,
                F.status,
                F.fastest_lap_rank
            FROM fact_race_results F
            JOIN dim_races R
                ON F.race_id = R.race_id
            JOIN dim_drivers D
                ON F.driver_id = D.driver_id
            """
    logger.info("Reading driver season base dataset from database")
    df = read_from_db_by_query(query)

    logger.info("Converting numeric columns")
    df['position'] = pd.to_numeric(df['position'], errors='coerce', downcast='integer')
    df['points'] = pd.to_numeric(df['points'], errors='coerce', downcast='integer')
    df['fastest_lap_rank'] = pd.to_numeric(df['fastest_lap_rank'], errors='coerce', downcast='integer')

    logger.info("Creating analytical indicator columns")
    df["is_win"] = (df["position"] == 1).astype(int)
    df["is_podium"] = (df["position"] <= 3).astype(int)
    df["is_dnf"] = (df["status"].str.strip().str.lower() == 'retired').astype(int)
    df["is_fastest_lap"] = (df["fastest_lap_rank"] == 1).astype(int)

    logger.info("Aggregating driver season statistics")
    driver_season_stats_df = df.groupby([
                                "season", 
                                "driver_id", 
                                "driver_first_name", 
                                "driver_last_name"
                                ]).agg(
                                    total_races = ("race_id", "count"),
                                    total_points = ("points", "sum"),
                                    wins = ("is_win", "sum"),
                                    podiums = ("is_podium", "sum"),
                                    dnf_count = ("is_dnf", "sum"),
                                    average_finish_position = ("position", lambda x: x.mean().round(2)),
                                    fastest_laps = ("is_fastest_lap", "sum")
                                ).reset_index()
    
    return driver_season_stats_df