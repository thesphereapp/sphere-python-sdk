import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from main.configuration.config_service import get_configuration_value

ca = certifi.where()


def get_client() -> MongoClient:
    """Returns the MongoDB client"""
    url = get_configuration_value("DB_URL")
    return MongoClient(url, server_api=ServerApi('1'), tlsCAFile=ca)
