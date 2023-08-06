from enum import Enum


class PreviewLanguage(str, Enum):
    PYTHON3 = "python3"
    DENO = "deno"
    GO = "go"
    BASH = "bash"
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)
