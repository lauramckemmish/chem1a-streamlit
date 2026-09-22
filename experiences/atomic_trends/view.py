"""Learner-facing Atomic trends observation surface."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from experiences.atomic_trends import data


PLOTLY_CONFIG = {
    "scrollZoom": False,
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d",
        "hoverClosestCartesian", "hoverCompareCartesian", "toggleSpikelines",
    ],
}
TRACE_COLOURS = ("#3F61C4", "#8A68C8", "#007882", "#B45309", "#BE185D", "#4D7C0F", "#475569")


def _figure(rows: list[dict[str, object]], property_label: str, units: str, show_labels: bool) -> go.Figure:
    """Build a bounded, evidence-first Plotly view without analytical tools."""
    property_key = data.PROPERTY_METADATA[property_label][0]
    figure = go.Figure()
    series_names = list(dict.fromkeys(str(row["series"]) for row in rows))
    for index, series_name in enumerate(series_names):
        series_rows = [row for row in rows if row["series"] == series_name]
        values = [float(row[property_key]) for row in series_rows]
        customdata = [
            [row["element_name"], row["symbol"], row["atomic_number"], row["period"], row["group"] or "—", value]
            for row, value in zip(series_rows, values)
        ]
        figure.add_trace(
            go.Scatter(
                x=[row["atomic_number"] for row in series_rows],
                y=values,
                name=series_name,
                mode="lines+markers+text" if show_labels else "lines+markers",
                text=[row["symbol"] for row in series_rows] if show_labels else None,
                textposition="top center",
                textfont={"size": 11},
                line={"color": TRACE_COLOURS[index % len(TRACE_COLOURS)], "width": 1.5},
                marker={"color": TRACE_COLOURS[index % len(TRACE_COLOURS)], "size": 8},
                customdata=customdata,
                hovertemplate=(
                    "<b>%{customdata[0]} (%{customdata[1]})</b><br>"
                    "Atomic number: %{customdata[2]}<br>Period: %{customdata[3]}<br>"
                    "Group: %{customdata[4]}<br>"
                    f"{property_label}: %{{customdata[5]:.4g}} {units}<extra></extra>"
                ),
            )
        )
    figure.update_layout(
        height=560,
        dragmode="zoom",
        hovermode="closest",
        template="plotly_white",
        margin={"l": 65, "r": 25, "t": 25, "b": 60},
        legend={"title": "Selection"},
    )
    figure.update_xaxes(title="Atomic number", dtick=1, showgrid=True, gridcolor="#E5E7EB")
    figure.update_yaxes(title=f"{property_label} / {units}", showgrid=True, gridcolor="#E5E7EB")
    return figure


def _subset_checkboxes(label: str, values: range, key_prefix: str, default: int, columns: int) -> list[int]:
    st.markdown(f"**{label}**")
    selected: list[int] = []
    for column, value in zip(st.columns(columns) * ((len(values) + columns - 1) // columns), values):
        if column.checkbox(str(value), value=value == default, key=f"{key_prefix}_{value}"):
            selected.append(value)
    return selected


def render() -> None:
    st.header("Explore periodic trends")
    st.write("Choose a property and a part of the periodic table.\n\nWhat pattern do you see?")

    property_label = st.selectbox("Property", list(data.PROPERTY_METADATA), key="atomic_trends_property")
    mode = st.selectbox("Explore", ["Periods", "Groups", "All elements"], key="atomic_trends_mode")
    if mode == "Periods":
        selections = _subset_checkboxes("Periods", range(1, 8), "atomic_trends_period", 2, 7)
    elif mode == "Groups":
        selections = _subset_checkboxes("Groups", range(1, 19), "atomic_trends_group", 1, 6)
    else:
        selections = []

    property_key, _, units = data.PROPERTY_METADATA[property_label]
    rows = data.series_for_selection(mode, selections, property_key)
    if not rows:
        st.info("Choose at least one period or group with available reference values.")
        return
    st.plotly_chart(_figure(rows, property_label, units, show_labels=mode != "All elements"), width="stretch", config=PLOTLY_CONFIG)
    table_rows = [
        {
            "Element": row["element_name"], "Symbol": row["symbol"], "Atomic number": row["atomic_number"],
            "Period": row["period"], "Group": row["group"], f"{property_label} ({units})": row[property_key],
        }
        for row in rows
    ]
    with st.expander("Data", expanded=False):
        st.dataframe(pd.DataFrame(table_rows), width="stretch", hide_index=True)
