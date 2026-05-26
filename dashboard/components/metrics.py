import streamlit as st


def render_driver_kpis(df_filtered):
    champion = (
        df_filtered.sort_values(by="total_points", ascending=False)
        .iloc[0]
    )

    most_wins = (
        df_filtered.sort_values(by="wins", ascending=False)
        .iloc[0]
    )

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Drivers", len(df_filtered))

        col2.metric(
            "Season Champion",
            f"{champion['driver_first_name']} {champion['driver_last_name']}",
        )

        with col3:
            st.metric(
                "Most Race Wins",
                f"{most_wins['driver_first_name']} {most_wins['driver_last_name']}",
            )
            st.caption(f"{int(most_wins['wins'])} wins")

    return champion, most_wins