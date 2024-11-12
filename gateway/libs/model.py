"""sumary_line

Keyword arguments:
argument -- description
Return: return_description

- response data:
  - status: str
  - user_id?: int
  - embedding?: list[float]
  - session?:
    - user_id: int
    - lock_id: int
    - startAt: float
    - endAt: float
"""
from pydantic import BaseModel
import time

from libs.database import fetch_session, insert_session, insert_user, search_user_by_embedding


class Session(BaseModel):
    user_id: str
    lock_id: str
    startAt: float
    endAt: float

class ResponseData(BaseModel):
    status: str
    user_id: str | None
    embedding: list[float] | None
    session: Session | None
    

def updateSession(resp: ResponseData):
    user_id = resp.user_id
    embedding = resp.embedding
    lock_id = resp.session.lock_id
    startAt = resp.session.startAt
    endAt = resp.session.endAt
    # update (user_id, embedding) to user Database
    insert_user(user_id, embedding)

    # update (user_id, lock_id, startAt, endAt) to Session Database
    insert_session(user_id, lock_id, startAt, endAt)


def sessionsValidation(sessions:list[tuple[float, float]]): 
    current = time.time()
    return any( session[0] <= current <= session[1] for session in sessions)

def userHasValidSession(user_id, lock_id, currentTime) -> bool:
    try:
        sessions = fetch_session(user_id, lock_id, currentTime) 
        print("success validate session")
        return bool(sessions) 
    except:
        print("fail validate session")
        return False
    
    

def getUserIdByEmbedding(embedding):
    user_id = search_user_by_embedding(embedding) 
    print(user_id)
    return user_id if user_id else -1