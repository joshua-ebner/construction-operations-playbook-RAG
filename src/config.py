import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
CHROMA_DIR = ROOT_DIR / "chroma_db"

CORPORA = ("safety", "maintenance", "quality")

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
TOP_K = 4


class Settings(BaseModel):
    portkey_api_key: str | None = None
    portkey_base_url: str = "https://portkeygateway.perficient.com/v1"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    use_portkey: bool = False
    llm_model: str = "gpt-4o-mini"
    anthropic_model: str = (
        "@aws-bedrock-use2/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    )
    embedding_model: str = "text-embedding-3-small"
    llm_provider: str = "openai"

    @classmethod
    def from_env(cls) -> "Settings":
        use_portkey = os.getenv("USE_PORTKEY", "").lower() in {"1", "true", "yes"}
        return cls(
            portkey_api_key=os.getenv("PORTKEY_API_KEY"),
            portkey_base_url=os.getenv(
                "PORTKEY_BASE_URL", "https://portkeygateway.perficient.com/v1"
            ),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            use_portkey=use_portkey,
            llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            anthropic_model=os.getenv(
                "ANTHROPIC_MODEL",
                "@aws-bedrock-use2/us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            ),
            embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
            llm_provider=os.getenv("LLM_PROVIDER", "openai").lower(),
        )

    @property
    def llm_api_key(self) -> str:
        if self.use_portkey:
            if not self.portkey_api_key:
                raise ValueError("USE_PORTKEY is set but PORTKEY_API_KEY is missing.")
            return self.portkey_api_key
        if self.llm_provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required for anthropic provider.")
            return self.anthropic_api_key
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for openai provider.")
        return self.openai_api_key

    @property
    def embedding_api_key(self) -> str:
        if self.use_portkey:
            if not self.portkey_api_key:
                raise ValueError("USE_PORTKEY is set but PORTKEY_API_KEY is missing.")
            return self.portkey_api_key
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for embeddings.")
        return self.openai_api_key

    @property
    def llm_base_url(self) -> str | None:
        return self.portkey_base_url if self.use_portkey else None

    @property
    def embedding_base_url(self) -> str | None:
        return self.portkey_base_url if self.use_portkey else None
