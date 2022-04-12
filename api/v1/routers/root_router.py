from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return "{}".format("WELCOME TO BLOG_API PROJECT."
                       "ADD /docs to the current url for swagger documentation and /redocs to the current url for redocs documentation.")
