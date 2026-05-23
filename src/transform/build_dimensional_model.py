import pandas as pd


def create_dim_drivers(df):
    dim_df_drivers = df[["driver_id","driver_code","driver_number","driver_first_name","driver_last_name","driver_nationality"]].copy()
    dim_df_drivers = dim_df_drivers.drop_duplicates(subset=["driver_id"])
    return dim_df_drivers


def create_dim_constructors(df):
    dim_df_constructors = df[["constructor_id","constructor_name","constructor_nationality"]].copy()
    dim_df_constructors = dim_df_constructors.drop_duplicates(subset=["constructor_id"])
    return dim_df_constructors


def create_dim_circuits(df):
    dim_df_circuits = df[["circuit_id","circuit_name","country","locality"]].copy()
    dim_df_circuits = dim_df_circuits.drop_duplicates(subset=["circuit_id"])
    return dim_df_circuits


def create_dim_races(df):
       dim_df_races = df[["season","round","race_name","race_date","circuit_id"]].copy()
       race_id = dim_df_races['season'].astype(str) + "_" + dim_df_races['round'].astype(str).str.zfill(2)
       
       dim_df_races.insert(
        loc=0,                       
        column='race_id',           
        value=race_id    
        )
       dim_df_races = dim_df_races.drop_duplicates(subset=["race_id"])

       return dim_df_races


def create_fact_race_results(df):
    fact_df_race_results = df[[
                            "season",
                            "round",
                            "driver_id",
                            "constructor_id",
                            "grid",
                            "position",
                            "position_text",
                            "points",
                            "laps",
                            "status",
                            "race_time",
                            "race_time_millis",         
                            "fastest_lap_rank",
                            "fastest_lap_lap",
                            "fastest_lap_time",
                            "fastest_lap_avg_speed"]]
    
    race_id = fact_df_race_results['season'].astype(str) + "_" + fact_df_race_results['round'].astype(str).str.zfill(2)
       
    fact_df_race_results.insert(
        loc=0,                       
        column='race_id',           
        value=race_id    
        )
    
    fact_df_race_results = fact_df_race_results.drop_duplicates(subset=["race_id","driver_id"])
    return fact_df_race_results