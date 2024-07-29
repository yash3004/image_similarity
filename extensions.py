import os
import spring_config
import spring_config.client
import yaml

_profile = os.getenv("PROFILE", "DEVELOPMENT")


def resolve_configuration():
    cfg_server = os.getenv("CONFIG_SERVER")
    if cfg_server:
        return _resolve_from_cloud_config(cfg_server)

    cfg_file = os.getenv("CONFIG_FILE", "config.yaml")
    with open(cfg_file, "r") as f:
        return yaml.load(f, yaml.SafeLoader)


def _resolve_from_cloud_config(cfg_server):
    config = (
        spring_config.ClientConfigurationBuilder()
        .app_name("course-generator-bridge")
        .address(cfg_server)
        .profile(_profile)
        .authentication((os.getenv("CONFIG_USERNAME"), os.getenv("CONFIG_PASSWORD")))
        .build()
    )

    return spring_config.client.SpringConfigClient(config)
