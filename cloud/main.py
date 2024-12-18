 
import pickle
from fastapi.responses import HTMLResponse
import numpy as np
from pydantic import BaseModel
import uvicorn  
from libs.facial import register_user, validate_user
from fastapi import FastAPI, File, Request 
from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel

class Data(BaseModel):
    lock_id: str
    embedding: list
 

def cloudFactory():
    app = FastAPI()  
    user1 = register_user(file_path='user1.jpg')
    users = [user1]
    
    templates = Jinja2Templates(directory="templates")


    @app.get('/', response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get('/admin', response_class=HTMLResponse)
    async def admin(request: Request):
        return templates.TemplateResponse("admin.html", {"request": request})

    @app.get('/user', response_class=HTMLResponse)
    async def user(request: Request):
        return templates.TemplateResponse("user.html", {"request": request})


    @app.post('/register/')
    async def facial_register(request: Request):
        received_data = await request.g
        embedding = pickle.load(received_data)
        users.append(embedding)

    @app.post('/api/unlock/')
    async def unlock(data: Data):
        unknown_embedding = data.embedding

        if validate_user(users, unknown_embedding):
            print('Approve user')
            return {'auth': 'approval'}
        else:
            print('Reject user')
            return {'auth': 'rejection'}
    return app
 



if __name__ == "__main__": 
    app = cloudFactory()
    uvicorn.run(app, host="0.0.0.0", port=8002)