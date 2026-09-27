import utils.clients
import utils.http_session
import utils.transport
import utils.session
import argparse
from agent import ShoppingAgent


def main():
    parser = argparse.ArgumentParser(description="Simple Safe Shopping Agent")
    parser.add_argument("--role", choices=["customer", "admin"], default=None,
                         help="Acting role, used for permission control")
    parser.add_argument("--request", default=None, help="Natural-language user request")
    args = parser.parse_args()

    role = args.role
    while role not in ("customer", "admin"):
        role = input("1) Enter role (customer/admin): ").strip().lower()

    request = args.request
    while not request:
        request = input("2) Enter your request: ").strip()

    agent = ShoppingAgent(role=role)

    print(f"\n=== Role: {role} ===")
    print(f"User request: {request}\n")

    answer = agent.run(request)

    print("--- Agent trace (tool calls) ---")
    if not agent.trace:
        print("(no tools were called)")
    for i, step in enumerate(agent.trace, 1):
        print(f"{i}. tool={step['tool']}  input={step['input']}")
        print(f"   result={step['result']}")

    print("\n--- Final answer ---")
    print(answer)


if __name__ == "__main__":
    main()
