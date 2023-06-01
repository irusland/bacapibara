from pydantic import BaseModel

from api.models.api.user_id import UserId
from api.models.key_value.announcement import Announcement


class AnnounceTask(BaseModel):
    announcement: Announcement
    to: UserId
