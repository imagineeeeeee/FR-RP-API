import requests
from fastapi import FastAPI

app = FastAPI()

# Configuration (Get these from Roblox Creator Dashboard)
ROBLOX_API_KEY = "YOUR_API_KEY_HERE"
UNIVERSE_ID = "YOUR_UNIVERSE_ID_HERE"

@app.get("/server/{server_code}")
def get_roblox_server_info(server_code: str):
    # Roblox Open Cloud URL for Memory Store
    url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/memory-store/sorted-maps/ActiveServers/items/{server_code}"
    
    headers = {"x-api-key": ROBLOX_API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Server not found or API error", "details": response.text}
