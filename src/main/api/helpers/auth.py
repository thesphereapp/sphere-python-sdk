from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from main.api.helpers.token_decode import SecurityHelper

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security_helper = SecurityHelper()


async def get_user_id(token: str = Depends(oauth2_scheme)) -> str:
    return security_helper.decode_token(token)["userId"]