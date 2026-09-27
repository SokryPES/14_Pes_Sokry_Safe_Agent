from pydantic import ValidationError
import tools
from schemas import (
    SearchProductsInput,
    CheckStockInput,
    BuyProductInput,
    DeleteProductInput,
)

PERMISSIONS = {
    "customer": {"search_products", "check_stock", "buy_product"},
    "admin": {"search_products", "check_stock", "buy_product", "delete_product"},
}

MAX_TOOL_CALLS = 6

TOOL_MODELS = {
    "search_products": SearchProductsInput,
    "check_stock": CheckStockInput,
    "buy_product": BuyProductInput,
    "delete_product": DeleteProductInput,
}

TOOL_FUNCS = {
    "search_products": tools.search_products,
    "check_stock": tools.check_stock,
    "buy_product": tools.buy_product,
    "delete_product": tools.delete_product,
}


def check_permission(role: str, tool_name: str) -> bool:
    return tool_name in PERMISSIONS.get(role, set())


def run_tool(role: str, tool_name: str, tool_input: dict) -> dict:
    """Validate permission + input, run the tool, and always return a
    structured result: {"ok": True, "data": ...} or
    {"ok": False, "error": CODE, "message": str}.
    Never raises — callers (agent.py) can safely feed the result back
    into the loop as an observation.
    """
    if tool_name not in TOOL_FUNCS:
        return {"ok": False, "error": "UNKNOWN_TOOL", "message": f"No such tool: {tool_name}"}

    if not check_permission(role, tool_name):
        return {
            "ok": False,
            "error": "PERMISSION_DENIED",
            "message": f"Role '{role}' is not allowed to call '{tool_name}'",
        }

    model = TOOL_MODELS[tool_name]
    try:
        validated = model(**tool_input)
    except ValidationError as e:
        return {"ok": False, "error": "INVALID_INPUT", "message": str(e)}

    try:
        result = TOOL_FUNCS[tool_name](**validated.model_dump())
        return {"ok": True, "data": result}
    except tools.ToolError as e:
        return {"ok": False, "error": "TOOL_ERROR", "message": str(e)}
    except Exception as e:  # last-resort guard, never leak raw tracebacks
        return {"ok": False, "error": "INTERNAL_ERROR", "message": str(e)}
