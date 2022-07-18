import aiohttp
import hikari
from sanic import Sanic
from sanic.exceptions import BadRequest
from sanic.response import json
from sanic_cors import CORS, cross_origin

from munchi.config import Config

from .routes import bp

app = Sanic("munchi-dashboard")
CORS(app)

# Register blueprints
app.blueprint(bp)


def main(
    host: str = "localhost",
    port: int = 8080,
    debug: bool = False,
    auto_reload: bool = False,
) -> None:
    auto_reload = debug or auto_reload or False

    app.run(host=host, port=port, debug=debug, auto_reload=auto_reload)


if __name__ == "__main__":
    main(debug=True)
