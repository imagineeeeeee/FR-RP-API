import os
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Roblox Server Tracker")

# Configuration
# It is better to set these in Render's "Environment Variables" 
# but I have hardcoded yours as requested for this test.
ROBLOX_API_KEY = "Be3bGQ0sBkSwQazP8JWl/E0c+9escbtOoPJSgpoeE3Z/3+YOZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaeTB5TURJeExUQTNMVEV6VkRFNE9qVXhPalE1V2lJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpTYjJKc2IzaEpiblJsY201aGJDSXNJbWx6Y3lJNklrTnNiM1ZrUVhWMGFHVnVkR2xqWVhScGIyNVRaWEoyYVdObElpd2lZbUZ6WlVGd2FVdGxlU0k2SWtKbE0ySkhVVEJ6UW10VGQxRmhlbEE0U2xkc0wwVXdZeXM1WlhOalluUlBiMUJLVTJkd2IyVkZNMW92TXl0WlR5SXNJbTkzYm1_REDACTED_FULL_KEY"
UNIVERSE_ID = "9727203097"

HEADERS = {"x-api-key": ROBLOX_API_KEY}

@app.get("/")
def home():
    return {"status": "API is running", "target_universe": UNIVERSE_ID}

@app.get("/server/{join_code}")
def get_server(join_code: str):
    """Fetch stats for one specific custom join code."""
    url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/memory-store/sorted-maps/ActiveServers/items/{join_code}"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        server_info = data.get("value", {})
        return {
            "join_code": join_code,
            "players": server_info.get("players", 0),
            "max_players": server_info.get("maxPlayers", 0),
            "last_updated": server_info.get("lastUpdate")
        }
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Server not found or expired")
    else:
        return {"error": "Roblox API Error", "code": response.status_code, "msg": response.text}

@app.get("/all-servers")
def list_servers():
    """List every active server and calculate total players."""
    url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/memory-store/sorted-maps/ActiveServers/items"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        items = response.json().get("items", [])
        active_list = []
        total_players = 0
        
        for item in items:
            val = item.get("value", {})
            p_count = val.get("players", 0)
            total_players += p_count
            
            active_list.append({
                "join_code": val.get("customCode"),
                "players": p_count,
                "max_players": val.get("maxPlayers", 0)
            })
            
        return {
            "universe_id": UNIVERSE_ID,
            "total_players_online": total_players,
            "server_count": len(active_list),
            "servers": active_list
        }
    return {"error": "Failed to fetch list", "details": response.text}
