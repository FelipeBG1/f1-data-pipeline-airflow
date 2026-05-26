import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from dashboard.queries import get_driver_season_stats
from dashboard.charts.driver_charts import create_top_drivers_points_chart
from dashboard.components.metrics import render_driver_kpis
from dashboard.components.insights import render_season_insight


st.set_page_config(
    page_title="F1 Analytics Dashboard",
    layout="wide",
)

st.title("F1 Analytics Dashboard")

df = get_driver_season_stats()

col1, col2 = st.columns([1, 3])

with col1:
    selected_season = st.selectbox(
        "Select season",
        sorted(df["season"].unique(), reverse=True),
    )

df_filtered = df[df["season"] == selected_season]

champion, most_wins = render_driver_kpis(df_filtered)

fig, top_drivers = create_top_drivers_points_chart(
    df_filtered,
    selected_season,
)

clean_config = {
    "displayModeBar": False,
    "showAxisDragHandles": False,
}

st.plotly_chart(
    fig,
    use_container_width=True,
    config=clean_config,
)

render_season_insight(
    df_filtered,
    champion,
    most_wins,
)

st.subheader("Driver Statistics Table")

df_table = top_drivers[
    [
        "driver_first_name",
        "driver_last_name",
        "total_points",
        "wins",
        "podiums",
        "average_finish_position",
    ]
].copy()

df_table["full_name"] = (
    df_table["driver_first_name"].astype(str)
    + " "
    + df_table["driver_last_name"].astype(str)
)

df_table = df_table[
    [
        "full_name",
        "total_points",
        "wins",
        "podiums",
        "average_finish_position",
    ]
]

st.dataframe(
    df_table,
    hide_index=True,
    height=250,
)