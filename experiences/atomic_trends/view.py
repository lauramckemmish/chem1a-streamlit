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
MAIN_GROUPS = (1, 2, 13, 14, 15, 16, 17, 18)


def _figure(
    rows: list[dict[str, object]],
    property_label: str,
    units: str,
    show_labels: bool,
    mode: str = "Periods",
    x_range: list[float] | None = None,
    show_xaxis: bool = True,
    height: int = 430,
) -> go.Figure:
    """Build a bounded, evidence-first Plotly view without analytical tools."""
    property_key = data.PROPERTY_METADATA[property_label][0]
    figure = go.Figure()
    series_names = list(dict.fromkeys(str(row["series"]) for row in rows))
    for index, series_name in enumerate(series_names):
        series_rows = [row for row in rows if row["series"] == series_name]
        values = [float(row[property_key]) if row[property_key] is not None else None for row in series_rows]
        x_values = [
            row["period"] if mode == "Groups" else row["group"] if mode == "Periods" else row["atomic_number"]
            for row in series_rows
        ]
        customdata = [
            [row["element_name"], row["symbol"], row["atomic_number"], row["period"], row["group"] or "—", value]
            for row, value in zip(series_rows, values)
        ]
        figure.add_trace(
            go.Scatter(
                x=x_values,
                y=values,
                name=series_name,
                mode="lines+markers+text" if show_labels else "lines+markers",
                text=[row["symbol"] for row in series_rows] if show_labels else None,
                textposition="top center",
                textfont={"size": 12},
                line={"color": TRACE_COLOURS[index % len(TRACE_COLOURS)], "width": 2},
                marker={"color": TRACE_COLOURS[index % len(TRACE_COLOURS)], "size": 9},
                connectgaps=False,
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
        height=height,
        dragmode="zoom",
        hovermode="closest",
        template="plotly_white",
        margin={"l": 60, "r": 18, "t": 15, "b": 50},
        showlegend=len(series_names) > 1,
        legend={"orientation": "h", "x": 0, "y": 1.05, "title": {"text": ""}},
    )
    if mode == "Periods":
        groups = sorted({int(row["group"]) for row in rows if row["group"] is not None})
        figure.update_xaxes(
            title="Group" if show_xaxis else None,
            tickmode="array",
            tickvals=groups,
            showgrid=False,
            showticklabels=show_xaxis,
            range=x_range,
        )
    elif mode == "Groups":
        figure.update_xaxes(
            title="Period" if show_xaxis else None,
            tickmode="array",
            tickvals=list(range(1, 8)),
            showgrid=False,
            showticklabels=show_xaxis,
            range=x_range or [0.5, 7.5],
        )
    else:
        figure.update_xaxes(
            title="Atomic number" if show_xaxis else None,
            showgrid=False,
            showticklabels=show_xaxis,
            range=x_range,
        )
    figure.update_yaxes(title=f"{property_label} / {units}", showgrid=True, gridcolor="#E5E7EB")
    return figure


def _x_domain(rows: list[dict[str, object]], mode: str) -> list[float] | None:
    """Derive the shared horizontal domain from the selected population."""
    if not rows:
        return None
    if mode == "Groups":
        return [0.5, 7.5]
    if mode == "Periods":
        positions = [int(row["group"]) for row in rows if row["group"] is not None]
    else:
        positions = [int(row["atomic_number"]) for row in rows]
    return [min(positions) - 0.5, max(positions) + 0.5] if positions else None


def _table_rows(
    rows: list[dict[str, object]],
    property_label: str,
    units: str,
    comparison_label: str | None = None,
    comparison_units: str | None = None,
) -> list[dict[str, object]]:
    """Present the complete selected slice, including unavailable values."""
    property_key = data.PROPERTY_METADATA[property_label][0]
    comparison_key = data.PROPERTY_METADATA[comparison_label][0] if comparison_label else None
    table_rows = []
    for row in rows:
        table_row = {
            "Element": row["element_name"], "Symbol": row["symbol"], "Atomic number": row["atomic_number"],
            "Period": row["period"], "Group": row["group"], f"{property_label} ({units})": row[property_key],
        }
        if comparison_key and comparison_label and comparison_units:
            table_row[f"{comparison_label} ({comparison_units})"] = row[comparison_key]
        table_rows.append(table_row)
    return table_rows


def _subset_checkboxes(label: str, values: range, key_prefix: str, default: int, columns: int) -> list[int]:
    st.markdown(f"**{label}**")
    selected: list[int] = []
    choices = list(values)
    for start in range(0, len(choices), columns):
        for column, value in zip(st.columns(columns), choices[start:start + columns]):
            if column.checkbox(str(value), value=value == default, key=f"{key_prefix}_{value}"):
                selected.append(value)
    return selected


def render() -> None:
    st.header("Periodic trends")

    property_column, comparison_column, mode_column = st.columns(3)
    property_label = property_column.selectbox("Property", list(data.PROPERTY_METADATA), key="atomic_trends_property")
    if st.session_state.get("atomic_trends_compare") == property_label:
        st.session_state["atomic_trends_compare"] = "None"
    comparison_options = ["None"] + [label for label in data.PROPERTY_METADATA if label != property_label]
    comparison_label = comparison_column.selectbox(
        "Compare with", comparison_options, key="atomic_trends_compare"
    )
    mode = mode_column.segmented_control(
        "Explore", ["Periods", "Groups", "All elements"], default="Periods", key="atomic_trends_mode"
    )
    if mode == "Periods":
        selections = _subset_checkboxes("Periods", range(1, 8), "atomic_trends_period", 2, 7)
    elif mode == "Groups":
        selections = _subset_checkboxes("Groups", MAIN_GROUPS, "atomic_trends_group", 1, 8)
    else:
        selections = []

    property_key, _, units = data.PROPERTY_METADATA[property_label]
    rows = data.series_for_selection(mode, selections, property_key)
    if not rows or not any(row[property_key] is not None for row in rows):
        st.info("Choose at least one period or group with available reference values.")
        return
    if comparison_label == "None":
        st.plotly_chart(
            _figure(rows, property_label, units, show_labels=mode != "All elements", mode=mode),
            width="stretch",
            config=PLOTLY_CONFIG,
        )
    else:
        _, _, comparison_units = data.PROPERTY_METADATA[comparison_label]
        x_range = _x_domain(rows, mode)
        st.plotly_chart(
            _figure(
                rows,
                property_label,
                units,
                show_labels=mode != "All elements",
                mode=mode,
                x_range=x_range,
                show_xaxis=False,
                height=340,
            ),
            width="stretch",
            config=PLOTLY_CONFIG,
        )
        st.plotly_chart(
            _figure(
                rows,
                comparison_label,
                comparison_units,
                show_labels=mode != "All elements",
                mode=mode,
                x_range=x_range,
                height=360,
            ),
            width="stretch",
            config=PLOTLY_CONFIG,
        )
    with st.expander("Data", expanded=False):
        comparison_units = data.PROPERTY_METADATA[comparison_label][2] if comparison_label != "None" else None
        table_comparison_label = comparison_label if comparison_label != "None" else None
        st.dataframe(
            pd.DataFrame(
                _table_rows(rows, property_label, units, table_comparison_label, comparison_units)
            ),
            width="stretch",
            hide_index=True,
        )
