from fastapi import APIRouter

router = APIRouter()

# Route to check is the backend server is working perfectly
@router.get("/live")
def live():
    try:
        return "I am available"
    except Exception as e:
        raise e