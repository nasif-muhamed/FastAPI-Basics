from fastapi import FastAPI, HTTPException, Response
from typing import List
from uuid import uuid4, UUID
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("850d034b-0c04-4f18-965d-e6db64da4983"),
        first_name="Muhamed",
        last_name="Savad",
        gender=Gender.male,
        roles=[Role.student]
    ), 
    User(
        id=UUID("e65078e5-73ab-4a35-b9d8-6abb96e12978"),
        first_name="Faris",
        last_name="Shamsu",
        gender=Gender.male,
        roles=[Role.admin, Role.student]
    )
]

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/api/v1/users/")
async def fetch_users():
    return db

@app.post("/api/v1/users/")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}/")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"detail": f"deleted user {user.first_name}"}
    raise HTTPException(
        status_code=404,
        detail=f"user with user_id: {user_id} does not exist"
    )
        
@app.put("/api/v1/user/{user_id}/")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
    raise HTTPException(
        status_code=404,
        detail=f"user with user_id: {user_id} does not exist"
    )
