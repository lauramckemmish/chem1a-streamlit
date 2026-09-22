"""Learner-facing Atomic trends observation surface."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from experiences.atomic_trends import data


def _chart(rows: list[dict[str, object]], property_label: str, units: str):
    frame = pd.DataFrame(rows)
    y_title = f"{property_label} / {units}"
    colour = alt.Color("series:N", title="Selection")
    x = alt.X("atomic_number:Q", title="Atomic number", axis=alt.Axis(tickMinStep=1))
    y = alt.Y(f"{data.PROPERTY_METADATA[property_label][0]}:Q", title=y_title)
    tooltip = [
        alt.Tooltip("element_name:N", title="Element"),
        alt.Tooltip("symbol:N", title="Symbol"),
        alt.Tooltip("atomic_number:Q", title="Atomic number"),
        alt.Tooltip("period:Q", title="Period"),
        alt.Tooltip("group:Q", title="Group"),
        alt.Tooltip(f"{data.PROPERTY_METADATA[property_label][0]}:Q", title=property_label, format=".4g"),
    ]
    lines = alt.Chart(frame).mark_line(opacity=0.38, strokeWidth=1.4).encode(x=x, y=y, color=colour, detail="series:N")
    points = alt.Chart(frame).mark_point(filled=True, size=75).encode(x=x, y=y, color=colour, tooltip=tooltip)
    labels = alt.Chart(frame).mark_text(dy=-11, fontSize=11).encode(x=x, y=y, text="symbol:N", color=colour, detail="series:N")
    return (lines + points + labels).properties(height=520).interactive()


def render() -> None:
    st.header("Explore periodic trends")
    st.write("Choose a property and a part of the periodic table.\n\nWhat pattern do you see?")

    property_label = st.selectbox("Property", list(data.PROPERTY_METADATA), key="atomic_trends_property")
    mode = st.selectbox("Explore", ["Periods", "Groups", "All elements"], key="atomic_trends_mode")
    if mode == "Periods":
        selections = st.multiselect("Period number", range(1, 8), default=[2], key="atomic_trends_periods")
    elif mode == "Groups":
        selections = st.multiselect("Group number", range(1, 19), default=[1], key="atomic_trends_groups")
    else:
        selections = []

    property_key, _, units = data.PROPERTY_METADATA[property_label]
    rows = data.series_for_selection(mode, selections, property_key)
    if not rows:
        st.info("Choose at least one period or group with available reference values.")
        return
    st.altair_chart(_chart(rows, property_label, units), width="stretch")
    table_rows = [
        {
            "Element": row["element_name"], "Symbol": row["symbol"], "Atomic number": row["atomic_number"],
            "Period": row["period"], "Group": row["group"], f"{property_label} ({units})": row[property_key],
        }
        for row in rows
    ]
    with st.expander("Data", expanded=False):
        st.dataframe(pd.DataFrame(table_rows), width="stretch", hide_index=True)
