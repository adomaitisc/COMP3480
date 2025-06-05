import argparse
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"


def root(args):
    resp = requests.get(f"{BASE_URL}/")
    print(resp.json())


def hello(args):
    resp = requests.get(f"{BASE_URL}/hello", params={"name": args.name})
    print(resp.json())


def sum_route(args):
    resp = requests.get(f"{BASE_URL}/sum/{args.one}/{args.two}")
    print(resp.json())


def wiki(args):
    resp = requests.get(f"{BASE_URL}/wiki/{args.topic}", allow_redirects=False)
    if resp.status_code in (302, 307):
        print({"redirect_to": resp.headers.get("location")})
    else:
        print(resp.json())


def weather(args):
    resp = requests.get(f"{BASE_URL}/weather", params={"city": args.city})
    print(resp.json())


def length(args):
    resp = requests.get(f"{BASE_URL}/length/{args.text}")
    print(resp.json())


def prime(args):
    resp = requests.get(f"{BASE_URL}/prime/{args.number}")
    print(resp.json())


def register(args):
    payload = {"name": args.name, "pin": args.pin}
    resp = requests.post(f"{BASE_URL}/register", json=payload)
    print(resp.json())


def login(args):
    payload = {"name": args.name, "pin": args.pin}
    resp = requests.post(f"{BASE_URL}/login", json=payload)
    print(resp.json())


def users_cookie(args):
    cookies = {}
    if args.token:
        cookies["token"] = args.token
    resp = requests.get(f"{BASE_URL}/users", cookies=cookies)
    print(resp.json())


def users_header(args):
    # send header "Authorization: Bearer <token>"
    headers = {"Authorization": f"Bearer {args.token}"}
    resp = requests.get(f"{BASE_URL}/users-header", headers=headers)
    print(resp.json())


def main():
    parser = argparse.ArgumentParser(description="CLI driver for FastAPI routes.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # GET /
    sp = subparsers.add_parser("root", help="GET /")
    sp.set_defaults(func=root)

    # GET /hello?name=<name>
    sp = subparsers.add_parser("hello", help="GET /hello?name=<name>")
    sp.add_argument("--name", required=True, help="Name to greet")
    sp.set_defaults(func=hello)

    # GET /sum/{one}/{two}
    sp = subparsers.add_parser("sum", help="GET /sum/{one}/{two}")
    sp.add_argument("--one", type=int, required=True, help="First integer")
    sp.add_argument("--two", type=int, required=True, help="Second integer")
    sp.set_defaults(func=sum_route)

    # GET /wiki/{topic}
    sp = subparsers.add_parser("wiki", help="GET /wiki/{topic} (redirect)")
    sp.add_argument("--topic", required=True, help="Wikipedia topic (use underscores)")
    sp.set_defaults(func=wiki)

    # GET /weather?city=<city>
    sp = subparsers.add_parser("weather", help="GET /weather?city=<city>")
    sp.add_argument("--city", default="Boston", help="City name (default=Boston)")
    sp.set_defaults(func=weather)

    # GET /length/{text}
    sp = subparsers.add_parser("length", help="GET /length/{text}")
    sp.add_argument("--text", required=True, help="Text to measure length")
    sp.set_defaults(func=length)

    # GET /prime/{number}
    sp = subparsers.add_parser("prime", help="GET /prime/{number}")
    sp.add_argument("--number", type=int, required=True, help="Number to check primality")
    sp.set_defaults(func=prime)

    # POST /register
    sp = subparsers.add_parser("register", help="POST /register")
    sp.add_argument("--name", required=True, help="Username to create")
    sp.add_argument("--pin", type=int, required=True, help="PIN as integer")
    sp.set_defaults(func=register)

    # POST /login
    sp = subparsers.add_parser("login", help="POST /login")
    sp.add_argument("--name", required=True, help="Username")
    sp.add_argument("--pin", type=int, required=True, help="PIN")
    sp.set_defaults(func=login)

    # GET /users (cookie-based)
    sp = subparsers.add_parser("users", help="GET /users (cookie‐based)")
    sp.add_argument("--token", help="Auth token (sent as cookie named 'token')")
    sp.set_defaults(func=users_cookie)

    # GET /users-header (header-based)
    sp = subparsers.add_parser(
        "users-header", help="GET /users-header (header‐based; use 'Bearer <token>')"
    )
    sp.add_argument("--token", required=True, help="Auth token (without 'Bearer ' prefix)")
    sp.set_defaults(func=users_header)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

