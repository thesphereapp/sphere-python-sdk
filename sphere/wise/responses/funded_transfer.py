import enum
from typing import Optional
from pydantic import Field, BaseModel


class FundedTransferStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class FundedTransferResponse(BaseModel):
    type: str = Field(alias="type")
    status: FundedTransferStatus = Field(alias="status")
    error_code: Optional[str] = Field(alias="errorCode")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "type": "BALANCE",
                    "status": "COMPLETED",
                    "errorCode": None
                }
        }
