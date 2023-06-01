from pydantic import BaseModel, constr


class Statement(BaseModel):
    content: constr(max_length=500)
