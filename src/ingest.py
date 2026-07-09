import re

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from src.config import CHROMA_DIR, CHUNK_OVERLAP, CHUNK_SIZE, CORPORA, DATA_DIR, Settings


def _extract_doc_id(text: str, fallback: str) -> str:
    match = re.search(r"\*\*Document ID:\*\*\s*(\S+)", text)
    return match.group(1) if match else fallback


def load_corpus_documents(corpus: str) -> list[Document]:
    corpus_dir = DATA_DIR / corpus
    documents: list[Document] = []

    for path in sorted(corpus_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        doc_id = _extract_doc_id(text, path.stem.upper())
        documents.append(
            Document(
                page_content=text,
                metadata={
                    "corpus": corpus,
                    "source": path.name,
                    "doc_id": doc_id,
                    "path": str(path.relative_to(DATA_DIR)),
                },
            )
        )
    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    return splitter.split_documents(documents)


def build_embeddings(settings: Settings) -> OpenAIEmbeddings:
    kwargs: dict = {
        "model": settings.embedding_model,
        "api_key": settings.embedding_api_key,
    }
    if settings.embedding_base_url:
        kwargs["base_url"] = settings.embedding_base_url
    return OpenAIEmbeddings(**kwargs)


def build_vectorstores(settings: Settings) -> dict[str, Chroma]:
    embeddings = build_embeddings(settings)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    stores: dict[str, Chroma] = {}

    for corpus in CORPORA:
        docs = load_corpus_documents(corpus)
        chunks = chunk_documents(docs)
        stores[corpus] = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=corpus,
            persist_directory=str(CHROMA_DIR / corpus),
        )
    return stores


def load_vectorstores(settings: Settings) -> dict[str, Chroma]:
    embeddings = build_embeddings(settings)
    stores: dict[str, Chroma] = {}

    for corpus in CORPORA:
        persist_dir = CHROMA_DIR / corpus
        if not persist_dir.exists():
            return build_vectorstores(settings)

        stores[corpus] = Chroma(
            collection_name=corpus,
            embedding_function=embeddings,
            persist_directory=str(persist_dir),
        )
    return stores
