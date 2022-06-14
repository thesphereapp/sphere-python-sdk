from typing import Optional

from fastapi.encoders import jsonable_encoder

from main.configuration.db_client import get_client

from main.domain.random.models.random_model import RandomModel


class RandomRepository:
    DATABASE_NAME = "Random"
    COLLECTION_NAME = "random_collection"
    INDEX_NAME = "my_index"

    def __init__(self, client=get_client()):
        self.database = client.get_database(self.DATABASE_NAME)
        self.collection = self.database[self.COLLECTION_NAME]

    def find_by_id(self, model_id:str) -> Optional[RandomModel]:
        result = self.collection.find_one({"_id": model_id})
        if result is None:
            return None
        return RandomModel(**result)

    def insert_one(self, model: RandomModel) -> Optional[RandomModel]:
        model_json = jsonable_encoder(model)
        self.collection.insert_one(model_json)
        return model

    def update_one_by_id(self, model: RandomModel):
        update_filter = {"_id": model.id}
        model = jsonable_encoder(model)
        update_command = {"$set": model}
        self.collection.update_one(update_filter, update_command, upsert=False)

    def delete_one_by_id(self, model: RandomModel):
        delete_filter = {"_id": model.id}
        self.collection.delete_one(delete_filter)
