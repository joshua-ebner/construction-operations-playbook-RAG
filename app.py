import streamlit as st

from src.config import Settings
from src.ingest import load_vectorstores
from src.rag import answer_question

CORPUS_LABELS = {
    "safety": "Safety Playbook",
    "maintenance": "Field Operations Playbook",
    "quality": "Quality Control Playbook",
}

EXAMPLE_QUESTIONS = [
    "What are the fall protection requirements above 6 feet on Level 14?",
    "How do I troubleshoot low concrete pump pressure during a pour?",
    "What are the rebar placement tolerances before a pour hold point?",
    "Can we continue steel erection during an active concrete cure hold?",
]

CUSTOM_CSS = """
<style>
    .block-container { padding-top: 1.5rem; max-width: 1100px; }
    .hero {
        background: linear-gradient(135deg, #0f2744 0%, #1a4a7a 100%);
        color: white; padding: 1.5rem 1.75rem; border-radius: 12px;
        margin-bottom: 1.25rem;
    }
    .hero h1 { margin: 0; font-size: 1.75rem; }
    .hero p { margin: 0.4rem 0 0; opacity: 0.9; }
    .route-badge {
        display: inline-block; background: #e8f1fb; color: #0f2744;
        border: 1px solid #b8d4f0; border-radius: 999px;
        padding: 0.35rem 0.85rem; font-weight: 600; font-size: 0.9rem;
    }
    .footer { color: #6b7280; font-size: 0.85rem; margin-top: 1rem; }
</style>
"""


@st.cache_resource(show_spinner="Indexing operations playbook...")
def get_vectorstores():
    settings = Settings.from_env()
    return load_vectorstores(settings), settings


def render_route(route):
    label = CORPUS_LABELS.get(route.corpus, route.corpus.title())
    st.markdown(
        f'<span class="route-badge">Routed to: {label} · {route.confidence} confidence</span>',
        unsafe_allow_html=True,
    )
    st.caption(route.rationale)


def render_answer(answer):
    st.subheader("Playbook Guidance")
    st.markdown(answer.summary)

    if answer.steps:
        st.markdown("**Action steps**")
        for i, step in enumerate(answer.steps, start=1):
            st.markdown(f"{i}. {step}")

    if answer.warnings:
        st.markdown("**Warnings**")
        for warning in answer.warnings:
            st.warning(warning)

    if answer.citations:
        st.markdown("**Source evidence**")
        for cite in answer.citations:
            with st.expander(f"{cite.doc_id} — {cite.source}"):
                st.write(cite.excerpt)

    st.caption(answer.limitations)


def main():
    st.set_page_config(
        page_title="Operations Playbook Assistant",
        page_icon="🏗️",
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero">
            <h1>Operations Playbook Assistant</h1>
            <p>Accelerate retrieval from safety, field ops, and QC playbooks — cited, actionable guidance for the jobsite.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "question" not in st.session_state:
        st.session_state.question = ""

    col1, col2 = st.columns([2, 1])
    with col1:
        st.session_state.question = st.text_input(
            "Search the operations playbook",
            value=st.session_state.question,
            placeholder="e.g. What are the fall protection requirements above 6 feet on Level 14?",
        )
    with col2:
        st.markdown("**Impact**")
        st.caption("Accelerate retrieval · Improve compliance · Standardize field decisions")

    st.markdown("**Try an example**")
    chip_cols = st.columns(2)
    for i, example in enumerate(EXAMPLE_QUESTIONS):
        if chip_cols[i % 2].button(example, key=f"ex_{i}", use_container_width=True):
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

            st.markdown("### Routing decision")
            render_route(route)
            render_answer(answer)
        except Exception as exc:
            st.error(f"Unable to generate answer: {exc}")
            st.info("Set OPENAI_API_KEY in .env for local testing.")

    st.markdown(
        '<p class="footer">Concept prototype · Answers grounded in operations playbook sections only · Not for production use without validation</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
