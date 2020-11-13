from pydantic import BaseModel
from starlette.responses import JSONResponse


class NotFoundSchema(BaseModel):
    message: str


class NotFound(JSONResponse):
    def __init__(self, message="not found"):
        super().__init__(
            status_code=404, content=NotFoundSchema(message=message).dict()
        )
