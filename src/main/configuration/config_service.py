import yaml
import os

from dotenv import load_dotenv

load_dotenv()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_mode() -> str:
    return os.getenv("MODE", "DEVELOPMENT")


def read_configuration(mode: str) -> any:
    file_path = {
        "DEVELOPMENT": os.path.join(__location__, 'development_config.yml'),
        "PRODUCTION": os.path.join(__location__, 'production_config.yml'),
    }
    config_file_path = file_path.get(mode, None)
    if config_file_path is None:
        raise ValueError("Unknown mode " + mode)
    with open(config_file_path, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config


DEVELOPMENT_CONFIGURATION = read_configuration("DEVELOPMENT")
PRODUCTION_CONFIGURATION = read_configuration("PRODUCTION")


def get_configuration_value(key: str, mode=get_mode()) -> any:
    match mode:
        case "PRODUCTION":
            return PRODUCTION_CONFIGURATION[key]
        case "DEVELOPMENT":
            return DEVELOPMENT_CONFIGURATION[key]
        case _:
            raise ValueError("Unknown mode " + mode)