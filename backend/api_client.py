# api_client.py
import requests

class CourtAPIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def start_session(self):
        """Initialize a new court session"""
        try:
            response = requests.post(f"{self.base_url}/start-session")
            return response.json()
        except:
            return {"error": "Could not connect to server"}
    
    def get_next_dialogue(self):
        """Get next dialogue from the agents"""
        try:
            response = requests.get(f"{self.base_url}/next-dialogue")
            return response.json()
        except:
            return {"error": "Could not get dialogue"}
            
    def trigger_action(self, action_type):
        """Trigger court action (pause, resume, etc)"""
        try:
            response = requests.post(f"{self.base_url}/action", 
                                   json={"action": action_type})
            return response.json()
        except:
            return {"error": "Could not trigger action"}