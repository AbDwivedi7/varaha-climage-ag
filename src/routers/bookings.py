from fastapi import APIRouter

router = APIRouter()

@router.get("/BookingsStart")
def live():
    try:
        return "Bookings Are Up"
    except Exception as e:
        raise e