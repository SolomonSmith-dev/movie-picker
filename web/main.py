from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MoviePicker API", 
    version="0.1.0",
    description="A smart movie recommendation API for your personal collection"
)

# Add CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to the MoviePicker API!",
        "docs": "/docs",
        "version": "0.1.0"
    }

# Include routers
from .routers import movies, users, recommendations
app.include_router(movies.router)
app.include_router(users.router)
app.include_router(recommendations.router)

# TODO: Add more routers
# from .routers import users, recommendations
# app.include_router(users.router)
# app.include_router(recommendations.router) 