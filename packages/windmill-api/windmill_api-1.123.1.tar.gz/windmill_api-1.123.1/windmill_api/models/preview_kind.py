from enum import Enum


class PreviewKind(str, Enum):
    CODE = "code"
    IDENTITY = "identity"
    GRAPHQL = "graphql"
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)
