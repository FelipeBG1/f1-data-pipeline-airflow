from src.transform.build_dimensional_model import create_dim_circuits,create_dim_constructors,create_dim_drivers,create_dim_races,create_fact_race_results
from src.load.read_from_db import read_from_db
from src.load.save_to_db import save_to_db
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)

def build_and_load_dimensional_model():
    logger.info("Creating dimensional tables")

    raw_race_results_df = read_from_db("raw_race_results")
    dim_drivers = create_dim_drivers(raw_race_results_df)
    dim_constructors = create_dim_constructors(raw_race_results_df)
    dim_circuits = create_dim_circuits(raw_race_results_df)
    dim_races = create_dim_races(raw_race_results_df)
    fact_race_results = create_fact_race_results(raw_race_results_df)

    logger.info("Saving dim_drivers table")
    save_to_db(dim_drivers,"dim_drivers")

    logger.info("Saving dim_constructors table")
    save_to_db(dim_constructors, "dim_constructors")

    logger.info("Saving dim_circuits table")
    save_to_db(dim_circuits, "dim_circuits")

    logger.info("Saving dim_races table")
    save_to_db(dim_races, "dim_races")

    logger.info("Saving fact_race_results table")
    save_to_db(fact_race_results, "fact_race_results")