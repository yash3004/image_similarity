import os

import qdrant_client
from flask import Flask, request, blueprints
import yaml

from flask_app.backflow.q_client import get_client


def create_app(client: qdrant_client.QdrantClient):
    app = Flask(__name__)
    config_file = os.environ.get("CONFIG_FILE", "../config.yaml")
    with open(config_file, "r") as cfg_file:
        config = yaml.load(cfg_file, yaml.loader.SafeLoader)
        app.config.update(config)

    from flask_app.backflow import q_client

    qdrant_client.init_client(app, client)

    return app


def main():
    client = get_client()
    app = create_app(client)


if __name__ == '__main__':
    main()
