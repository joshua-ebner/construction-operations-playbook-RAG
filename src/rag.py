from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from src.config import TOP_K, Settings
from src.models import Citation, CorpusName, RouteDecision, SupervisorAnswer
from src.router import build_llm, route_question


ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an AI assistant that retrieves answers from the operations playbook for site superintendents on construction jobsites.

Answer ONLY using the provided playbook context for the routed corpus: {corpus}.

Return a concise operational answer with:
- summary: 2-3 sentences
- steps: numbered action steps when applicable
- warnings: safety or quality caveats
- citations: quote short supporting excerpts with source file and doc_id

If context is insufficient, say what is missing. Do not invent procedures.""",
        ),
        (
            "human",
            """Question: {question}

Routing rationale: {rationale}

Context:
{context}""",
        ),
    ]
)


def format_context(documents: list[Document]) -> str:
    blocks: list[str] = []
    for idx, doc in enumerate(documents, start=1):
        meta = doc.metadata
        blocks.append(
            f"[{idx}] doc_id={meta.get('doc_id')} source={meta.get('source')}\n{doc.page_content}"
        )
    return "\n\n---\n\n".join(blocks)


def retrieve(
    vectorstores: dict[str, Chroma], corpus: CorpusName, question: str
) -> list[Document]:
    return vectorstores[corpus].similarity_search(question, k=TOP_K)


def generate_answer(
    question: str,
    route: RouteDecision,
    documents: list[Document],
    settings: Settings,
) -> SupervisorAnswer:
    llm = build_llm(settings)
    chain = ANSWER_PROMPT | llm.with_structured_output(SupervisorAnswer)
    answer = chain.invoke(
        {
            "question": question,
            "corpus": route.corpus,
            "rationale": route.rationale,
            "context": format_context(documents),
        }
    )

    if not answer.citations and documents:
        answer.citations = [
            Citation(
                source=doc.metadata.get("source", "unknown"),
                doc_id=doc.metadata.get("doc_id", "unknown"),
                excerpt=doc.page_content[:240].strip() + "...",
            )
            for doc in documents[:2]
        ]
    return answer


def answer_question(
    question: str,
    vectorstores: dict[str, Chroma],
    settings: Settings,
) -> tuple[RouteDecision, SupervisorAnswer, list[Document]]:
    route = route_question(question, settings)
    documents = retrieve(vectorstores, route.corpus, question)
    answer = generate_answer(question, route, documents, settings)
    return route, answer, documents
