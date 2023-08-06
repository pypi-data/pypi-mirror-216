from enum import Enum


class GetCompletedJobResponse200JobKind(str, Enum):
    SCRIPT = "script"
    PREVIEW = "preview"
    DEPENDENCIES = "dependencies"
    FLOW = "flow"
    FLOWPREVIEW = "flowpreview"
    SCRIPT_HUB = "script_hub"
    IDENTITY = "identity"
    HTTP = "http"
    GRAPHQL = "graphql"
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)
