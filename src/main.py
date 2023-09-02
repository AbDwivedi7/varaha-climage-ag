import uvicorn

from fastapi import FastAPI

from routers import ( bookings, building, live, users, organizations )

# Making a FastAPI App
app = FastAPI()

# All the Routers
app.include_router(live.router, tags=["Liveness Probe"]) # Liveness Router
app.include_router(users.router, tags=["Users"]) # Users Router
app.include_router(building.router, tags=["Rooms"]) # Rooms Router
app.include_router(bookings.router, tags=["Bookings"]) # Bookings Router
app.include_router(organizations.router, tags=["Organizations"]) # Organization Router

if __name__ == "__main__":
    # Serving the FastAPI App through uvicorn
    uvicorn.run("main:app", port=8000, reload=True)