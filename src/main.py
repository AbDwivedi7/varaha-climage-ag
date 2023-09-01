import uvicorn

from fastapi import FastAPI

from routers import ( bookings, live, rooms, users )

# Making a FastAPI App
app = FastAPI()


# All the Routers
app.include_router(live.router, tags=["Liveness Probe"]) # Liveness Router
app.include_router(users.router, tags=["Users"]) # Users Router
app.include_router(rooms.router, tags=["Rooms"]) # Rooms Router
app.include_router(bookings.router, tags=["Bookings"]) # Bookings Probe

if __name__ == "__main__":
    # Serving the FastAPI App through uvicorn
    uvicorn.run("main:app", port=8000, reload=True)