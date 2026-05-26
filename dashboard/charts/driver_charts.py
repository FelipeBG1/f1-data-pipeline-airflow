import plotly.express as px


def create_top_drivers_points_chart(df, selected_season):
    top_drivers = (
        df.sort_values(by="total_points", ascending=False)
        .head(10)
        .copy()
    )
    top_drivers["full_name"] = (
        top_drivers["driver_first_name"].astype(str)
        + " "
        + top_drivers["driver_last_name"].astype(str)
    )

    driver_order = top_drivers["full_name"].tolist()

    fig = px.bar(
        top_drivers,
        x="full_name",
        y="total_points",
        labels={
            "full_name": "Driver",
            "total_points": "Points",
        },
        text_auto="d",
        color="full_name",
        category_orders={
            "full_name": driver_order
        },
        template="plotly_dark",
    )

    fig.update_layout(
        height=350,
        showlegend=False,
        title={
            "text": f"Top 10 Drivers by Points — {selected_season}",
            "font": {"size": 28},
        },
    )

    return fig, top_drivers