import os
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Roblox Server Tracker")

# Configuration
# It is better to set these in Render's "Environment Variables" 
# but I have hardcoded yours as requested for this test.
ROBLOX_API_KEY = "4l3/+/OHwUmB49rEGtxDALJEI4Rwh7X2of9tZeZ1LVKncTujZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaeTB5TURJeExUQTNMVEV6VkRFNE9qVXhPalE1V2lJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpTYjJKc2IzaEpiblJsY201aGJDSXNJbWx6Y3lJNklrTnNiM1ZrUVhWMGFHVnVkR2xqWVhScGIyNVRaWEoyYVdObElpd2lZbUZ6WlVGd2FVdGxlU0k2SWpSc015OHJMMDlJZDFWdFFqUTVja1ZIZEhoRVFVeEtSVWswVW5kb04xZ3liMlk1ZEZwbFdqRk1Wa3R1WTFSMWFpSXNJbTkzYm1WeVNXUWlPaUl4TlRRd01qUTRNRFV6SWl3aVpYaHdJam94TnpjeU1EazNOVEV5TENKcFlYUWlPakUzTnpJd09UTTVNVElzSW01aVppSTZNVGMzTWpBNU16a3hNbjAuYXJaVWd1eVdidTZ3SnRDRldYYVllcEZ2UnB0LUR6aEx2T244VXdzRnUyMDdZNGtZbVVjakYyX3dqb2NYNVJVZmw4RWN5UUpfWVp6blE4OU1MN18wUklJT0VkUWJuQ0c4UE84ZEtIVEQ2SnBkXzhCbFY4YnV6ZGlHNGk5YlRHQ2RMX1hKeVREUnk2YVJXY3FHeDIzSFZDZ0JFbWFON1ZfdEZ1cWtVOWlac2VxUTJ3NUtwQ3NyRkJmYzBuVHhEV3BvNUttNlRhbE9kc2hTTllLUUUzcFN2djlHNU1ORkVRUHNRYURzdi11THFhT0dkbWRWc2pSVGdtLVlMaGtibWg2Wk11SU1JVzNfM2RuLXU5WE9JY1RIZGd0aExGY3hDVGViNWpPYzVYRnQxX0VYXzljZllBaXA4YXVucktVUlJZa0dXTW02Rk1hbjdScER2OXVEdVFMY0NR"
UNIVERSE_ID = "9727203097"

@app.get("/server/{join_code}")
def get_server(join_code: str):
    url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/memory-store/sorted-maps/ActiveServers/items/{join_code}"
    headers = {"x-api-key": ROBLOX_API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        stats = data.get("value", {})
        return {
            "players": stats.get("players", 0),
            "max_players": stats.get("maxPlayers", 0)
        }
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Server not found or expired")
    return {"error": "Roblox API Error", "status": response.status_code}

@app.get("/debug/all")
def list_all():
    # Use this to see what codes actually exist right now
    url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/memory-store/sorted-maps/ActiveServers/items"
    headers = {"x-api-key": ROBLOX_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()
