"""Small shared visual conventions for CHEM 1A learner experiences.

The palette and prompt treatment are adapted from the canonical UNSW educational
app starter. UNSW yellow is reserved for compact rules, borders, and state markers;
routine controls avoid large solid-yellow surfaces. Experience-specific pedagogy and
scientific rendering remain local.
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
        .st-key-chem1a_compare_prompt, .st-key-chem1a_absorption_prompt, .st-key-chem1a_absorption_question {{
            background: #f7f5fb;
            border-left: 4px solid var(--chem1a-purple);
            margin-top: 0.9rem;
            padding: 0.7rem 1rem 0.55rem;
        }}
        .st-key-chem1a_hard_reveal_wavelength_scale, .st-key-chem1a_hard_reveal_absorption {{
            border-left: 3px solid var(--chem1a-purple);
            margin: 0.9rem 0 0.8rem;
            padding: 0.2rem 0 0.2rem 0.8rem;
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
        [class*="st-key-chem1a_absorption_pair_"] {{
            margin: 0.35rem 0 0.65rem;
        }}
        .chem1a-pair-atom {{
            color: #17212b;
            font-weight: 650;
            margin: 0.2rem 0 0.1rem;
        }}
        .chem1a-pair-label {{
            color: #475569;
            font-size: 0.85rem;
            font-weight: 650;
            margin: 0.1rem 0 0;
        }}
        [role="tab"] {{
            color: #17212b !important;
        }}
        [role="tab"] p {{
            color: inherit !important;
        }}
        [role="tab"][aria-selected="true"] {{
            color: #17212b !important;
            font-weight: 650;
        }}
        [role="tab"][aria-selected="true"] p {{
            font-weight: 650 !important;
        }}
        [class*="st-key-chem1a_hard_reveal_"] button {{
            background: transparent !important;
            border: 2px solid var(--chem1a-yellow) !important;
            color: #17212b !important;
            font-weight: 650;
        }}
        [class*="st-key-chem1a_hard_reveal_"] button:hover {{
            background: rgba(255, 220, 0, 0.10) !important;
            border-color: var(--chem1a-yellow) !important;
            color: #17212b !important;
        }}
        button:focus-visible {{
            outline: 3px solid var(--chem1a-black) !important;
            outline-offset: 2px;
            box-shadow: 0 0 0 5px var(--chem1a-yellow) !important;
        }}
        label:has(input[type="checkbox"])[data-selected="true"] > div:first-of-type {{
            background: var(--chem1a-purple) !important;
            border-color: var(--chem1a-purple) !important;
        }}
        label:has(input[type="checkbox"])[data-selected="true"] > div:first-of-type svg {{
            stroke: #ffffff !important;
        }}
        label:has(input[type="checkbox"]:focus-visible) > div:first-of-type {{
            outline: 3px solid var(--chem1a-black);
            outline-offset: 2px;
            box-shadow: 0 0 0 5px var(--chem1a-yellow);
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


def stage_selector(labels: list[str], *, key: str, default_index: int = 0) -> str:
    """Render a compact local selector within an experience."""
    if st.session_state.get(key) not in labels:
        st.session_state[key] = labels[default_index]
    return st.segmented_control(
        "Spectroscopy stage",
        labels,
        default=st.session_state[key],
        key=key,
        label_visibility="collapsed",
    )


def hard_reveal(prompt: str, *, key: str, reveal_label: str) -> bool:
    """Persist a consequential evidence reveal without adding a completion gate."""
    st.session_state.setdefault(key, False)
    with st.container(key=f"chem1a_hard_reveal_{key}"):
        st.write(prompt)
        if not st.session_state[key]:
            st.button(
                reveal_label,
                type="primary",
                key=f"{key}_button",
                on_click=lambda: st.session_state.__setitem__(key, True),
            )
            return False
    return True
