from typing import Optional
from fastapi import APIRouter

from app.services.managers.search import TransfermarktManagerSearch


router = APIRouter()

@router.get("/search/{manager_name}")
def search_managers(manager_name: str, page_number: Optional[int] = 1):
    tfmkt = TransfermarktManagerSearch(query=manager_name, page_number=page_number)
    found_players = tfmkt.search_managers()
    return found_players