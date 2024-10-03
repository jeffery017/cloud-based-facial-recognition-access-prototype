import base64
import requests
import uvicorn 
import json
import numpy as np

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from libs.facial import encode_face
from libs.ip import get_local_ip


class Data(BaseModel):
    lock_id: str
    image: str


def gatewayFactory():
    app = FastAPI()

    @app.get('/')
    async def index():
        return {"hello": "world"}

    @app.post('/api/unlock/')
    async def facial_recognition(data: Data): 
        print('receive a unlock request')  

        # get image 
        filename = "uploaded_snapshot.jpg" 
        with open(filename, "wb") as f: 
            image = base64.b64decode(data.image)
            f.write(image)
        
        # encode the face to embedding
        encoding = encode_face(filename)
        data = {
            'lock_id': data.lock_id,
            'encoding': np.array2string( encoding)
            }
        json_data = json.dumps(data)
            
        # request authentication from cloud db
        url = f'http://{get_local_ip()}:8002/api/unlock/'
        response = requests.post(url, data=json_data)


        # return result
        if response.headers.get('Content-Type') == 'application/json':
            return response.json()
        return {'auth': 'rejection'}
    
    return app
    
 
    

 


if __name__ == "__main__": 
    app = gatewayFactory()
    uvicorn.run(app, host="0.0.0.0", port=8001)