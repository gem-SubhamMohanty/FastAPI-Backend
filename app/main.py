from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth,vote

# create the database tables
# models.Base.metadata.create_all(bind=engine)

# fastapi is the library and we are importing module.
app = FastAPI()  # creating an instance of fast API

origins = ["https://www.google.com","https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")   # decorator #root path
async def root():  # async is used for making an API call or talking to the database/ path operation function
    # fast api converts it to json
    return {"message": "Hello World. I am subham Mohanty. I love chelsea football club."}

# adding routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
