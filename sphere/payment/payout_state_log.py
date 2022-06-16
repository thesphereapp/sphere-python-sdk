from datetime import datetime, timezone
from pydantic import BaseModel

from sphere.payment.payout_state import PayoutState


class PayoutStateLog(BaseModel):
    state: PayoutState = PayoutState.NEW
    date: datetime = datetime.now(timezone.utc)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "state": "NEW",
                "date": "2022-03-10 07:00:00.550604",
            }
        }
