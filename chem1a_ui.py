"""Small shared visual conventions for CHEM 1A learner experiences.

The palette and prompt treatment are adapted from the canonical UNSW educational
app starter. Experience-specific pedagogy and scientific rendering remain local.
"""

from __future__ import annotations

import streamlit as st


UNSW_COLOURS = {
    "yellow": "#FFDC00",
    "black": "#000000",
    "indigo": "#3F61C4",
    "purple": "#8A68C8",
    "teal": "#007882",
}


def apply_shared_visual_system() -> None:
    """Apply the small, robust subset of the shared UNSW visual system in use now."""
    st.markdown(
        f"""
        <style>
        :root {{
            --chem1a-yellow: {UNSW_COLOURS["yellow"]};
            --chem1a-black: {UNSW_COLOURS["black"]};
            --chem1a-purple: {UNSW_COLOURS["purple"]};
        }}
        .st-key-chem1a_stage_controls {{
            border-left: 4px solid var(--chem1a-yellow);
            margin: 0.4rem 0 0.7rem;
            padding: 0.15rem 0 0.1rem 0.8rem;
        }}
        .chem1a-control-label {{
            color: #17212b;
            font-size: 0.9rem;
            font-weight: 650;
            letter-spacing: 0.01em;
            margin: 0.05rem 0 0.25rem;
        }}
        .st-key-chem1a_compare_prompt, .st-key-chem1a_absorption_prompt {{
            background: #f7f5fb;
            border-left: 4px solid var(--chem1a-purple);
            margin-top: 0.9rem;
            padding: 0.7rem 1rem 0.55rem;
        }}
        .chem1a-prompt-label {{
            color: #4f3b74;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin: 0 0 0.15rem;
            text-transform: uppercase;
        }}
        .chem1a-prompt-text {{
            color: #17212b;
            font-size: 1.05rem;
            margin: 0;
        }}
        input[type="checkbox"]:focus-visible {{
            box-shadow: 0 0 0 4px var(--chem1a-yellow);
            outline: 3px solid var(--chem1a-black);
            outline-offset: 2px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def compare_prompt(text: str, *, key: str = "chem1a_compare_prompt") -> None:
    """Render the shared, quiet prompt treatment for an observational comparison."""
    with st.container(key=key):
        st.markdown('<p class="chem1a-prompt-label">Compare</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="chem1a-prompt-text">{text}</p>', unsafe_allow_html=True)
