import base64
from fastapi import FastAPI, File, Form, Request
import requests
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn 
from libs.camera_control import capture, generate_frames
from libs.ip import get_local_ip
 
app = FastAPI()
url = get_local_ip()
port = 8000

templates = Jinja2Templates(directory="templates")

# Define a route that responds with an HTML file
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Render the 'index.html' template and pass a variable (name) to it
    return templates.TemplateResponse("index.html", {"request": request, "name": "FastAPI User"})



@app.post("/unlock/")
async def handle_unlock(request: Request):
    print('receive a unlock request')
    # take a picture
    filename = 'snapshot.jpg'
    result = capture(filename) 
    # post to gateway
    filepath = f'./{filename}'
    url = f'http://{get_local_ip()}:8001/api/unlock/'
    result = send_image(filepath, url)

    # receive approval and return to client
    print(result)
    return result #{'auth': 'approval'}
    


def send_image(image_path, url): 
    with open(image_path, 'rb') as file:
        encoded_image = encode_image_to_base64(image_path)
        
        # files = {'file': file}
        data = {
            'lock_id' :'device_1',
            'image': encoded_image
        }
        
        response = requests.post(url, json=data)
        print(response)
        if response.status_code == 200:
            try:
                json_content = response.json()  # Parse the response as JSON
                return json_content  # Return the JSON content
            except ValueError:
                return {"error": "Response is not valid JSON"}  # Handle JSON parsing errors
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
 
    

def encode_image_to_base64(image_path: str) -> str:
    """Encode an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')




if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000)