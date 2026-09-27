class ToolError(Exception):
    """Recoverable, tool-level failure (e.g. OUT_OF_STOCK, NOT_FOUND)."""

PRODUCTS = [
    {"id": 1, "name": "Dell XPS 13 Laptop", "category": "laptop", "price": 999.99, "stock": 5},
    {"id": 2, "name": "MacBook Air M2", "category": "laptop", "price": 1199.00, "stock": 0},
    {"id": 3, "name": "Logitech Wireless Mouse", "category": "accessory", "price": 25.50, "stock": 50},
    {"id": 4, "name": "Mechanical Keyboard", "category": "accessory", "price": 89.99, "stock": 12},
    {"id": 5, "name": "27-inch 4K Monitor", "category": "monitor", "price": 329.99, "stock": 7},
    {"id": 6, "name": "USB-C Hub", "category": "accessory", "price": 49.99, "stock": 20},
    {"id": 7, "name": "External SSD 1TB", "category": "storage", "price": 149.99, "stock": 15},
    {"id": 8, "name": "Gaming Chair", "category": "furniture", "price": 199.99, "stock": 3}
]


def _find_product(product_id: int):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def search_products(query: str) -> list[dict]:
    q = query.lower()
    return [p for p in PRODUCTS if q in p["name"].lower() or q in p["category"].lower()]


def check_stock(product_id: int) -> dict:
    p = _find_product(product_id)
    if not p:
        raise ToolError(f"PRODUCT_NOT_FOUND: no product with id {product_id}")
    return {"product_id": p["id"], "name": p["name"], "stock": p["stock"]}


def buy_product(product_id: int, quantity: int) -> dict:
    p = _find_product(product_id)
    if not p:
        raise ToolError(f"PRODUCT_NOT_FOUND: no product with id {product_id}")
    if p["stock"] < quantity:
        raise ToolError(f"OUT_OF_STOCK: only {p['stock']} unit(s) left for {p['name']}")
    p["stock"] -= quantity
    return {
        "product_id": p["id"],
        "name": p["name"],
        "purchased": quantity,
        "remaining_stock": p["stock"],
    }


def delete_product(product_id: int) -> dict:
    p = _find_product(product_id)
    if not p:
        raise ToolError(f"PRODUCT_NOT_FOUND: no product with id {product_id}")
    PRODUCTS.remove(p)
    return {"deleted_product_id": product_id, "name": p["name"]}
