from datetime import datetime, date
from pydantic import BaseModel


class IATABase(BaseModel):
    code: str


class IATACreate(IATABase):
    pass


class IATAUpdate(IATABase):
    pass


class IATAInDB(IATABase):
    id: int

    class Config:
        orm_mode = True


class IATA(IATAInDB):
    pass
