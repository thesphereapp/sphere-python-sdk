from fastapi import HTTPException

from main.domain.random.models.random_model import RandomModel
from main.domain.random.repository.random_repository import RandomRepository


class RandomService:
    random_repository = RandomRepository

    def __init__(self):
        self.random_repository = RandomRepository()

    def insert(self, model: RandomModel):
        self.random_repository.insert_one(model)

    def get_random(self, model_id: str) -> RandomModel:
        model = self.random_repository.find_by_id(model_id)
        if model is None:
            raise HTTPException(status_code=404, detail="Model {} not found".format(model_id))
        return model
