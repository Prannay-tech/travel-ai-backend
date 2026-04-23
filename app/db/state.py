from typing import Dict, Any

# In a real app this would be Redis/PostgreSQL
class MemoryDatabase:
    def __init__(self):
        self.sessions: Dict[str, Any] = {}
        self.users: Dict[str, Any] = {}
        self.tokens: Dict[str, str] = {}

    def get_session(self, session_id: str) -> Any:
        return self.sessions.get(session_id)

    def set_session(self, session_id: str, data: Any):
        self.sessions[session_id] = data

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

db = MemoryDatabase()
