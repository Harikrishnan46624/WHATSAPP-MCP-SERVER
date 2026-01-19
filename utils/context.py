from fastmcp.server.middleware import MiddlewareContext


def get_session_id() -> str:
    try:
        ctx = MiddlewareContext.current()
        return getattr(ctx, "session_id", None) or "default"
    except Exception:
        return "default"
