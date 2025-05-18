active_sessions = set()

def add_active_session(chat_id: int):
    active_sessions.add(chat_id)
    print(f"Active sessions after add: {active_sessions}")

def remove_active_session(chat_id: int):
    active_sessions.discard(chat_id)
    print(f"Active sessions after remove: {active_sessions}")

def get_active_sessions():
    result = list(active_sessions)
    print(f"Returning active sessions: {result}")
    return result