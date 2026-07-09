import streamlit as st

from src.config import Settings
from src.ingest import load_vectorstores
from src.rag import answer_question

CORPUS_LABELS = {
    "safety": "Safety Playbook",
    "maintenance": "Field Operations Playbook",
    "quality": "Quality Control Playbook",
}

PLAYBOOK_NAV = [
    ("safety", "Safety Playbook"),
    ("maintenance", "Field Operations Playbook"),
    ("quality", "Quality Control Playbook"),
]

EXAMPLE_QUESTIONS = [
    "What are the fall protection requirements above 6 feet on Level 14?",
    "How do I troubleshoot low concrete pump pressure during a pour?",
    "What are the rebar placement tolerances before a pour hold point?",
    "Can we continue steel erection during an active concrete cure hold?",
]

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --suffolk-navy: #0c1d36;
        --suffolk-navy-mid: #1a3a5c;
        --suffolk-red: #e30613;
        --suffolk-gray-bg: #ececec;
        --suffolk-gray-panel: #f5f5f5;
        --suffolk-text: #1a2b3c;
        --suffolk-muted: #6b7c8f;
        --suffolk-border: #d4d4d4;
    }

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .stApp {
        background-color: var(--suffolk-gray-bg);
    }

    #MainMenu, footer, header[data-testid="stHeader"] {
        visibility: hidden;
    }

    .block-container {
        padding-top: 0 !important;
        max-width: 1100px;
    }

    .top-bar {
        background: var(--suffolk-navy);
        color: white;
        padding: 0.85rem 1.75rem;
        margin: -1rem -1rem 0 -1rem;
        width: calc(100% + 2rem);
    }

    .app-title {
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .hero-panel {
        background: var(--suffolk-gray-panel);
        border: 1px solid var(--suffolk-border);
        padding: 1.75rem 1.75rem 1.5rem;
        margin-bottom: 1.5rem;
    }

    .section-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--suffolk-muted);
        margin-bottom: 0.75rem;
    }

    .section-label .sq {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: var(--suffolk-red);
        flex-shrink: 0;
    }

    .hero-panel h1 {
        margin: 0;
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--suffolk-navy);
        line-height: 1.2;
    }

    .hero-sub {
        margin: 0.6rem 0 0;
        color: var(--suffolk-muted);
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .side-panel {
        background: white;
        border: 1px solid var(--suffolk-border);
        padding: 1rem 1.1rem;
        height: 100%;
    }

    .playbook-nav {
        list-style: none;
        padding: 0;
        margin: 0.5rem 0 0;
    }

    .playbook-nav li {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid var(--suffolk-border);
        font-size: 0.85rem;
        color: var(--suffolk-muted);
    }

    .playbook-nav li:last-child {
        border-bottom: none;
    }

    .playbook-nav .sq {
        display: inline-block;
        width: 7px;
        height: 7px;
        background: var(--suffolk-navy);
        flex-shrink: 0;
    }

    .impact-text {
        margin: 0.5rem 0 0;
        font-size: 0.82rem;
        color: var(--suffolk-muted);
        line-height: 1.6;
    }

    .route-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: white;
        color: var(--suffolk-navy);
        border: 1px solid var(--suffolk-border);
        padding: 0.45rem 0.85rem;
        font-weight: 600;
        font-size: 0.88rem;
    }

    .route-badge .sq {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: var(--suffolk-red);
        flex-shrink: 0;
    }

    .answer-section-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--suffolk-muted);
        margin: 1.25rem 0 0.5rem;
    }

    .answer-section-label .sq {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: var(--suffolk-red);
    }

    .answer-heading {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--suffolk-navy);
        margin: 0 0 0.75rem;
    }

    .footer {
        color: var(--suffolk-muted);
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--suffolk-border);
    }

    div[data-testid="stTextInput"] input {
        border-radius: 0 !important;
        border-color: var(--suffolk-border) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: var(--suffolk-navy) !important;
        box-shadow: 0 0 0 1px var(--suffolk-navy) !important;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background-color: var(--suffolk-navy) !important;
        color: white !important;
        border-radius: 0 !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: var(--suffolk-navy-mid) !important;
    }

    div[data-testid="stButton"] button[kind="secondary"] {
        background-color: white !important;
        color: var(--suffolk-text) !important;
        border: 1px solid var(--suffolk-border) !important;
        border-radius: 0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.82rem !important;
        text-align: left !important;
        white-space: normal !important;
        height: auto !important;
        min-height: 2.75rem;
        padding: 0.6rem 0.75rem !important;
    }

    div[data-testid="stButton"] button[kind="secondary"]:hover {
        border-left: 3px solid var(--suffolk-red) !important;
        border-color: var(--suffolk-border) !important;
    }

    div[data-testid="stExpander"] {
        border: 1px solid var(--suffolk-border) !important;
        border-radius: 0 !important;
        background: white !important;
    }

    .stSpinner > div {
        border-top-color: var(--suffolk-navy) !important;
    }
</style>
"""


def section_label(text: str) -> str:
    return f'<div class="section-label"><span class="sq"></span>{text}</div>'


def render_playbook_nav() -> str:
    items = "".join(
        f'<li><span class="sq"></span>{label}</li>' for _, label in PLAYBOOK_NAV
    )
    return f'<ul class="playbook-nav">{items}</ul>'


@st.cache_resource(show_spinner="Indexing operations playbook...")
def get_vectorstores():
    settings = Settings.from_env()
    return load_vectorstores(settings), settings


def render_route(route):
    label = CORPUS_LABELS.get(route.corpus, route.corpus.title())
    st.markdown(
        f'<span class="route-badge"><span class="sq"></span>'
        f'Routed to: {label} · {route.confidence} confidence</span>',
        unsafe_allow_html=True,
    )
    st.caption(route.rationale)


def render_answer(answer):
    st.markdown(
        section_label("PLAYBOOK GUIDANCE") + '<p class="answer-heading">Field Guidance</p>',
        unsafe_allow_html=True,
    )
    st.markdown(answer.summary)

    if answer.steps:
        st.markdown(section_label("ACTION STEPS"), unsafe_allow_html=True)
        for i, step in enumerate(answer.steps, start=1):
            st.markdown(f"{i}. {step}")

    if answer.warnings:
        st.markdown(section_label("WARNINGS"), unsafe_allow_html=True)
        for warning in answer.warnings:
            st.warning(warning)

    if answer.citations:
        st.markdown(section_label("SOURCE EVIDENCE"), unsafe_allow_html=True)
        for cite in answer.citations:
            with st.expander(f"{cite.doc_id} — {cite.source}"):
                st.write(cite.excerpt)

    st.caption(answer.limitations)


def main():
    st.set_page_config(
        page_title="Operations Playbook Assistant",
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="top-bar">
            <span class="app-title">Operations Playbook Assistant</span>
        </div>
        <div class="hero-panel">
        """
        + section_label("THE OPERATIONS PLAYBOOK")
        + """
            <h1>How can we help your jobsite?</h1>
            <p class="hero-sub">Accelerate retrieval from safety, field ops, and QC playbooks —
            cited, actionable guidance for the jobsite.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "question" not in st.session_state:
        st.session_state.question = ""

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(section_label("SEARCH THE PLAYBOOK"), unsafe_allow_html=True)
        st.session_state.question = st.text_input(
            "Search the operations playbook",
            value=st.session_state.question,
            placeholder="e.g. What are the fall protection requirements above 6 feet on Level 14?",
            label_visibility="collapsed",
        )
    with col2:
        st.markdown(
            '<div class="side-panel">'
            + section_label("PLAYBOOK CORPORA")
            + render_playbook_nav()
            + section_label("IMPACT")
            + '<p class="impact-text">Accelerate retrieval · Improve compliance · '
            "Standardize field decisions</p>"
            + "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(section_label("TRY AN EXAMPLE"), unsafe_allow_html=True)
    chip_cols = st.columns(2)
    for i, example in enumerate(EXAMPLE_QUESTIONS):
        if chip_cols[i % 2].button(
            example, key=f"ex_{i}", use_container_width=True, type="secondary"
        ):
            st.session_state.question = example
            st.rerun()

    ask = st.button("Get Answer", type="primary", disabled=not st.session_state.question)

    if ask and st.session_state.question:
        try:
            vectorstores, settings = get_vectorstores()
            with st.spinner("Routing question and retrieving documentation..."):
                route, answer, _docs = answer_question(
                    st.session_state.question, vectorstores, settings
                )

            st.markdown(
                section_label("ROUTING DECISION"),
                unsafe_allow_html=True,
            )
            render_route(route)
            render_answer(answer)
        except Exception as exc:
            st.error(f"Unable to generate answer: {exc}")
            st.info(
                "Check OPENAI_API_KEY in Railway Variables (or .env for local testing)."
            )

    st.markdown(
        '<p class="footer">Concept prototype · Answers grounded in operations playbook '
        "sections only · Not for production use without validation</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
