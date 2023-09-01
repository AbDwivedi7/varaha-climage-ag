from fastapi import APIRouter

router = APIRouter()

@router.get("/RoomsStart")
def live():
    try:
        return "Rooms are Up"
    except Exception as e:
        raise e