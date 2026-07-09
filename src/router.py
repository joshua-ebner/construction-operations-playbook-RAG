from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import Settings
from src.models import RouteDecision


ROUTER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You route jobsite superintendent questions to the correct operations playbook corpus.

Corpora:
- safety: fall protection, excavation, crane lifts, PPE, incident response, OSHA
- maintenance: equipment inspections, crane PM, concrete pump troubleshooting, tool crib
- quality: pour inspection, rebar tolerances, hold points, punch list, NCR disposition

Choose the corpus that should AUTHORITATIVELY answer the question.
If a question spans areas, pick the corpus that should lead the response.""",
        ),
        ("human", "{question}"),
    ]
)


def build_llm(settings: Settings) -> ChatOpenAI:
    model = (
        settings.anthropic_model
        if settings.llm_provider == "anthropic"
        else settings.llm_model
    )
    kwargs: dict = {
        "model": model,
        "api_key": settings.llm_api_key,
        "temperature": 0,
    }
    if settings.llm_base_url:
        kwargs["base_url"] = settings.llm_base_url
    return ChatOpenAI(**kwargs)


def route_question(question: str, settings: Settings) -> RouteDecision:
    llm = build_llm(settings)
    chain = ROUTER_PROMPT | llm.with_structured_output(RouteDecision)
    return chain.invoke({"question": question})
