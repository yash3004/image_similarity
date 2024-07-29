import os

from flask import Flask, request, blueprints
import yaml


def create_app():
    app = Flask(__name__)
    config_file = os.environ.get("CONFIG_FILE", "../config.yaml")
    with open(config_file, "r") as cfg_file:
        config = yaml.load(cfg_file, yaml.loader.SafeLoader)
        app.config.update(config)


    return app


def main():
    app = create_app()


if __name__ == '__main__':
    main()
