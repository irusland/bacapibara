from pydantic import BaseModel

from api.models.key_value.announcement import Announcement


class Announcements(BaseModel):
    announcements: list[Announcement]
