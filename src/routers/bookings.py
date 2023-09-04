from fastapi import APIRouter

router = APIRouter()

@router.get("/booking/book")
def book():
    try:
        return True
    except Exception as e:
        raise e