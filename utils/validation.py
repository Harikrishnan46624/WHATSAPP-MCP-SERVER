from mcp import McpError
from mcp.types import ErrorData


def require_exactly_one(**kwargs):
    provided = [k for k, v in kwargs.items() if v]
    if len(provided) != 1:
        raise McpError(
            ErrorData(
                code=400,
                message=f"Provide exactly one of {list(kwargs.keys())}",
            )
        )
