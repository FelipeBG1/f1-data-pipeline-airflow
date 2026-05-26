import streamlit as st


def build_season_insight(df_filtered, champion, most_wins):
    sorted_df = df_filtered.sort_values(by="total_points", ascending=False)

    runner_up = sorted_df.iloc[1]

    champion_name = (
        f"{champion['driver_first_name']} {champion['driver_last_name']}"
    )

    most_wins_name = (
        f"{most_wins['driver_first_name']} {most_wins['driver_last_name']}"
    )

    runner_up_name = (
        f"{runner_up['driver_first_name']} {runner_up['driver_last_name']}"
    )

    points_gap = champion["total_points"] - runner_up["total_points"]

    if champion_name != most_wins_name:
        return (
            f"{champion_name} won the championship despite fewer race wins than "
            f"{most_wins_name}, highlighting consistency across the season."
        )

    if points_gap <= 10:
        return (
            f"{champion_name} led both points and race wins, "
            f"but finished only {int(points_gap)} points ahead of {runner_up_name}."
        )

    return (
        f"{champion_name} led both points and race wins, "
        f"finishing {int(points_gap)} points ahead of {runner_up_name}."
    )


def render_season_insight(df_filtered, champion, most_wins):
    insight_text = build_season_insight(df_filtered, champion, most_wins)
    st.info(insight_text)