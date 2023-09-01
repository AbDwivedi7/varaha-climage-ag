from fastapi import APIRouter

router = APIRouter()


@router.get("/UsersStart")
def live():
    try:
        return "Users Are Up"
    except Exception as e:
        raise e