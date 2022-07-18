import argparse
import logging

from rich.logging import RichHandler

from dashboard.backend import app

parser = argparse.ArgumentParser("backend")
parser.add_argument("--host", help="Server host", type=str, default="0.0.0.0")
parser.add_argument("--port", help="Server port", type=int, default=8080)
parser.add_argument(
    "--dev", help="Launch in development mode", type=bool, default=False
)
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])

app.main(host=args.host, port=args.port, debug=args.dev)
