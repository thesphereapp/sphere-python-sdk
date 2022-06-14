from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from main.domain.random.models.random_model import RandomModel
from main.domain.random.random_service import RandomService
from fastapi import Depends, APIRouter
from main.api.helpers.auth import get_user_id
from main.api.random.requests.random_form import RandomForm

random_router = APIRouter(
    prefix="/v1/random",
    tags=["Random"],
    responses={404: {"description": "Nothing was found"}},
)

random_service = RandomService()


@random_router.get("/task/{random_id}")
async def get_random(random_id: str, user_id: str = Depends(get_user_id)):
    random = random_service.get_random(random_id)
    random = jsonable_encoder(random)
    return JSONResponse(status_code=status.HTTP_200_OK, content=random)


@random_router.post("/task")
async def post_random(random_form: RandomForm):
    insert_form = RandomModel(id=None, name=random_form.email, createdDateUtc=None, isFixed=False)
    random_service.insert(insert_form)
    return JSONResponse(status_code=status.HTTP_201_CREATED)
