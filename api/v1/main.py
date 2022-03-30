# import uvicorn
from fastapi import FastAPI


from api.v1.db.models import user_model as models
from api.v1.db.config import engine
from api.v1.routers import user_router, post_router, comment_router, reply_router
from api.v1 import __version__

app = FastAPI(title="API", description="API for a simple blog",
              version=__version__)
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
app.include_router(reply_router.router)


@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)


# if __name__ == '__main__':
#     uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
