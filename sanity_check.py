import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class EnvironmentCheck(BaseModel):
    openai_key_present: bool
    anthropic_key_present: bool
    langsmith_key_present: bool


def main() -> None:
    check = EnvironmentCheck(
        openai_key_present=bool(os.getenv("OPENAI_API_KEY")),
        anthropic_key_present=bool(os.getenv("ANTHROPIC_API_KEY")),
        langsmith_key_present=bool(os.getenv("LANGSMITH_API_KEY")),
    )

    print(check.model_dump())


if __name__ == "__main__":
    main()
