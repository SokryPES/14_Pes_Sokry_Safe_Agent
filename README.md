# Simple Safe Shopping Agent

This is a small shopping agent. You can ask it to search
for products, check stock, buy a product, or delete a product.

The agent is rule-based. It does not use an AI API, an API key, or an internet
connection. The function `decide_next_action()` in `agent.py` acts as the
agent's brain.

## How it works

1. You write a request in normal words.
2. The agent chooses a tool.
3. `harness.py` checks permission and input data.
4. The tool runs and returns a result.
5. The agent reads the result and gives a final answer.

The application code controls every tool call. This means a user cannot use a
tool that their role does not allow.

## Install

You need Python and the Pydantic package.

```bash
pip install pydantic
```

No API key is needed.

## Run the program

Start the interactive program:

```bash
python main.py
```

The program asks for a role and a request. For example:

```text
1) Enter role (customer/admin): customer
2) Enter your request: Find a laptop that is currently in stock
```

## Available tools

| Tool                                | What it does |
| `search_products(query)`            | Finds products by name or category. |
| `check_stock(product_id)`           | Shows the current stock for one product. |
| `buy_product(product_id, quantity)` | Buys a product when enough stock is available. |
| `delete_product(product_id)`        | Deletes a product from the catalog. Admin only. |

## User roles

| Tool              | Customer | Admin |
| `search_products` | Yes      | Yes |
| `check_stock`     | Yes      | Yes |
| `buy_product`     | Yes      | Yes |
| `delete_product`  | No       | Yes |

Permissions are checked in `harness.py`. For example, if a customer tries to
delete a product, the tool does not run. The program returns
`PERMISSION_DENIED` instead.

## Example result

Command:

```bash
python main.py 
role: customer 
request: "Find a laptop that is currently in stock"
```

The agent searches for laptops, checks the stock of the first result, and can
print an answer like this:

```text
Found 'Dell XPS 13 Laptop' ($999.99), in stock: 5 units.
```

More complete examples are in `demo_output.txt`.

## Safety features

- Pydantic checks the tool input before a tool runs.
- Product IDs and quantities must be greater than zero.
- Tool errors are returned as simple error messages.
- Customers cannot delete products.
- The agent can make no more than six tool calls in one request.

## Project files

```text
README.md        This guide
main.py          Starts the command-line program
agent.py         Agent loop and decision rules
tools.py         Product data and shopping actions
schemas.py       Input rules for each tool
harness.py       Permissions, validation, and error handling
demo_output.txt  Example terminal output
```
