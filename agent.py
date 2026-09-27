import re
from harness import run_tool, MAX_TOOL_CALLS


class ShoppingAgent:
    def __init__(self, role: str = "customer"):
        self.role = role
        self.trace = []  # list of {tool, input, result} for this run

    def run(self, user_request: str) -> str:
        self.trace = []
        history = []

        for _ in range(MAX_TOOL_CALLS):
            decision = decide_next_action(user_request, history)

            if decision["action"] == "final":
                return decision["answer"]

            tool_name = decision["tool"]
            tool_input = decision["input"]
            result = run_tool(self.role, tool_name, tool_input)

            step = {"tool": tool_name, "input": tool_input, "result": result}
            self.trace.append(step)
            history.append(step)

        return "Stopped: reached the maximum tool-call limit without a final answer."


def decide_next_action(user_request: str, history: list) -> dict:
    """The agent's 'brain'. Looks at the request plus every tool call
    made so far (history) and returns either:
      {"action": "call_tool", "tool": <name>, "input": {...}}
    or
      {"action": "final", "answer": <str>}
    """
    text = user_request.lower()
    called = {h["tool"] for h in history}

    
    if "delete" in text or "remove" in text:
        if "delete_product" not in called:
            pid = _extract_int(text)
            return {"action": "call_tool", "tool": "delete_product",
                     "input": {"product_id": pid if pid is not None else -1}}
        result = history[-1]["result"]
        if result["ok"]:
            d = result["data"]
            return {"action": "final", "answer": f"Deleted product #{d['deleted_product_id']} ({d['name']})."}
        return {"action": "final", "answer": f"Could not delete product: {result['error']} - {result['message']}"}

    
    if "buy" in text or "purchase" in text:
        if "buy_product" not in called:
            pid = _extract_int(text, occurrence=1)
            qty = _extract_int(text, occurrence=2) or 1
            return {"action": "call_tool", "tool": "buy_product",
                     "input": {"product_id": pid if pid is not None else -1, "quantity": qty}}
        result = history[-1]["result"]
        if result["ok"]:
            d = result["data"]
            return {"action": "final",
                     "answer": f"Bought {d['purchased']} x {d['name']}. Remaining stock: {d['remaining_stock']}."}
        return {"action": "final", "answer": f"Could not buy product: {result['error']} - {result['message']}"}

    
    if "search_products" not in called:
        keyword = _extract_keyword(text)
        return {"action": "call_tool", "tool": "search_products", "input": {"query": keyword}}

    search_step = next(h for h in history if h["tool"] == "search_products")
    if not search_step["result"]["ok"] or not search_step["result"]["data"]:
        keyword = search_step["input"]["query"]
        return {"action": "final", "answer": f"No products found for '{keyword}'."}

    first = search_step["result"]["data"][0]

    if "check_stock" not in called:
        return {"action": "call_tool", "tool": "check_stock", "input": {"product_id": first["id"]}}

    stock_step = next(h for h in history if h["tool"] == "check_stock")
    if stock_step["result"]["ok"] and stock_step["result"]["data"]["stock"] > 0:
        stock = stock_step["result"]["data"]["stock"]
        return {"action": "final",
                 "answer": f"Found '{first['name']}' (${first['price']}), in stock: {stock} units."}
    return {"action": "final", "answer": f"Found '{first['name']}' but it is currently out of stock."}


def _extract_int(text: str, occurrence: int = 1):
    nums = re.findall(r"\d+", text)
    if len(nums) >= occurrence:
        return int(nums[occurrence - 1])
    return None


def _extract_keyword(text: str) -> str:
    for word in ["laptop", "macbook", "dell", "mouse", "keyboard", "accessory"]:
        if word in text:
            return word
    words = text.strip().split()
    return words[-1] if words else text
