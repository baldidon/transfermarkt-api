from typing import Optional
from fastapi import APIRouter

from app.services.managers.search import TransfermarktManagerSearch
from app.services.managers.profile import TransfermarktManagerProfile

router = APIRouter()

@router.get("/search/{manager_name}")
def search_managers(manager_name: str, page_number: Optional[int] = 1):
    tfmkt = TransfermarktManagerSearch(query=manager_name, page_number=page_number)
    found_players = tfmkt.search_managers()
    return found_players

@router.get("/{manager_id}/profile")
def get_manager_profile(manager_id: str):
    tfmkt = TransfermarktManagerProfile(manager_id=manager_id)
    found_players = tfmkt.get_manager_profile()
    return found_players