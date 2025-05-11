
from pyodk.client import Client
import toml
from pathlib import Path

def get_odk_client():
    config_path = Path(__file__).resolve().parents[1] / "config.toml"
    config = toml.load(config_path)
    odk_config = config["central"]
    print(odk_config["base_url"])
    client = Client(
        url=odk_config["base_url"],
        username=odk_config["username"],
        password=odk_config["password"],
        default_project_id=odk_config["default_project_id"]
    )
    return client
