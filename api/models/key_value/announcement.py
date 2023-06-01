from datetime import datetime

from pydantic import BaseModel

from api.models.api.user_id import UserId
from api.models.key_value.statement import Statement


class Announcement(BaseModel):
    statement: Statement
    by: UserId
    at: datetime
