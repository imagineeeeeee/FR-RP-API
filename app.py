from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# This defines the structure of the data we expect to receive
class User(BaseModel):
    name: str
    email: str

@app.get("/")
def read_root():
    return {"message": "Hello! My API is officially live on Render."}

# This is your new POST method
@app.post("/create-user")
def create_user(user: User):
    # In a real app, you would save this to a database here
    return {
        "status": "User created successfully!",
        "received_data": {
            "name": user.name,
            "email": user.email
        }
    }
