import base64
import random
from typing import Optional
import numpy
import requests
import uvicorn  
import time
import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from libs.database import create_session_table, create_users_table, insert_session, insert_user
from libs.model import getUserIdByEmbedding, userHasValidSession
from libs.facial import encode_face 

 

useLocalCache = 0

class Data(BaseModel):
    lock_id: int
    image: str

user_number = 500
def initSessions():
    startAt = time.time()
    endAt = startAt + 3600 
    users = list(range(user_number))
    locks = list(range(10))
    random.shuffle(users) 
    random.shuffle(locks)
    for user in users:
        for lock in locks:
            insert_session(user_id=user, lock_id=lock, startAt=startAt, endAt=endAt)

def initUsers():
    for i in range(user_number):
        embedding = numpy.random.rand(128)
        # print(embedding)
        insert_user(i, embedding)



def gatewayFactory():
    app = FastAPI()
    create_session_table()
    create_users_table()
    initSessions()
    initUsers()

    @app.get('/')
    async def index():
        return {"hello": "world"}

    @app.post('/api/unlock/')
    async def facial_recognition(data: Data): 
        # startAt = time.time()
        print('receive a unlock request!')  
        lock_id = data.lock_id 
        
        # get image 
        filename = "uploaded_snapshot.jpg" 
        with open(filename, "wb") as f: 
            image = base64.b64decode(data.image)
            f.write(image)
        # encode the face to embedding
        embedding = encode_face(filename)
        
        
        
        user_id = getUserIdByEmbedding(embedding)
        user_id = 1
        print(user_id)
        if user_id > 0 and userHasValidSession(user_id, lock_id, time.time()):
            return { 'status': 'APPROVAL' }
             

        # generate request header and data
        headers = {"Content-Type": "application/json"}
        data = {
            'user_id': -1,
            'lock_id': data.lock_id, 
            'embedding': embedding.tolist()
            } 
        
        # request authentication from cloud db
        #url = f'http://localhost:8005/unlock/'
        url = "http://3.143.141.44:8000/unlock"
        print(f"send request to {url}")
        response = requests.post(url, headers=headers,json=data)
            
        
        # return result
        if response.headers.get('Content-Type') == 'application/json':
            print("receive success response")
            response = response.json() 
            res = { 'status': response['status'] }
            # print(f'{(time.time() - startAt)*1000:.2f}')
            return res
        
        # print(f'{(time.time() - startAt)*1000:.2f}')
        
        return {'status': 'REJECTION'}

    return app
    



if __name__ == "__main__": 
    app = gatewayFactory()
    uvicorn.run(app, host="0.0.0.0", port=8006)