from fastapi import APIRouter

router = APIRouter()

@router.get("/live")
def live():
    try:
        return "I am available"
    except Exception as e:
        raise e