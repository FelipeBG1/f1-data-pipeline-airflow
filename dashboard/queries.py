from src.load.read_from_db import read_from_db_by_query


def get_driver_season_stats():
    query = """
        SELECT
            season,
            driver_first_name,
            driver_last_name,
            total_points,
            wins,
            podiums,
            average_finish_position
        FROM driver_season_stats
        ORDER BY total_points DESC
    """

    return read_from_db_by_query(query, ".env.dashboard")