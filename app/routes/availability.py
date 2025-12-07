from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter

router = APIRouter(prefix="/availability", tags=["availability"])


def generate_dummy_slots() -> List[dict]:
    start = datetime.now().replace(minute=0, second=0, microsecond=0)
    slots = []
    for i in range(5):
        slot_start = start + timedelta(hours=i)
        slot_end = slot_start + timedelta(minutes=30)
        slots.append({"start": slot_start.isoformat(), "end": slot_end.isoformat()})
    return slots


@router.get("")
def get_availability() -> List[dict]:
    return generate_dummy_slots()
