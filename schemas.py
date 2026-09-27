from pydantic import BaseModel, Field

class SearchProductsInput(BaseModel):
    query: str = Field(..., min_length=1, description="Search term, e.g. product name or category")

class CheckStockInput(BaseModel):
    product_id: int = Field(..., gt=0, description="Positive product ID")

class BuyProductInput(BaseModel):
    product_id: int = Field(..., gt=0, description="Positive product ID")
    quantity: int = Field(..., gt=0, description="Positive quantity to purchase")

class DeleteProductInput(BaseModel):
    product_id: int = Field(..., gt=0, description="Positive product ID")


TOOL_SCHEMAS = [
    {
        "name": "search_products",
        "description": "Search the product catalog by name or category keyword.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term, e.g. 'laptop'"}
            },
            "required": ["query"],
        },
    },
    {
        "name": "check_stock",
        "description": "Check current stock quantity for a specific product ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "Positive product ID"}
            },
            "required": ["product_id"],
        },
    },
    {
        "name": "buy_product",
        "description": "Purchase a quantity of a product. Reduces stock if enough is available.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "Positive product ID"},
                "quantity": {"type": "integer", "description": "Positive quantity to purchase"},
            },
            "required": ["product_id", "quantity"],
        },
    },
    {
        "name": "delete_product",
        "description": "Permanently remove a product from the catalog. Admin only.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "Positive product ID"}
            },
            "required": ["product_id"],
        },
    },
]
