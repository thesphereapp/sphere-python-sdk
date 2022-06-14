from datetime import datetime
from typing import Dict

from main.configuration.config_service import get_configuration_value
from fastapi import HTTPException
import jwt


class SecurityHelper:
    jwt_secret = get_configuration_value("JWT")["SECRET"]

    def decode_token(self, token: str) -> Dict[str, any]:
        decoded_result = self.__decode(token)
        if decoded_result is None:
            raise HTTPException(status_code=401, detail="Authentication failed")

        expiry_time = decoded_result.get("expiryTimeStampUtc", None)
        if expiry_time is None:
            raise HTTPException(status_code=401, detail="Authentication has expired. Please log in")
        expiry_time = datetime.fromisoformat(expiry_time)
        if expiry_time < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Authentication has expired. Please log in")
        return decoded_result

    def __decode(self, encoded: any) -> Dict[str, any]:
        return jwt.decode(encoded, self.jwt_secret, algorithms=["HS256"])
