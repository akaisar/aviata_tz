from typing import List, Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import UJSONResponse

from app import crud
from app.api.utils.db import get_db
from app.api.utils.errors import NotFoundSchema, NotFound
from app.schemas.ticket import Ticket


router = APIRouter()


@router.get("/", response_model=List[Ticket], response_class=UJSONResponse)
def list_(
    db: Session = Depends(get_db),
):
    tickets = crud.ticket.get_multi(db)
    return tickets
