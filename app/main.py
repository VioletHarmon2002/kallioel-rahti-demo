from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]  # allow all origins, change later to real origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


my_name = "Liza"




# main route
@app.get("/")
def read_root():
    return { "msg": f"Hello, {my_name}" }

# what is my ip route
@app.get("/api/ip")
def api_ip(request: Request):
    return { "ip": request.client.host }


@app.get("/ip", response_class=HTMLResponse)
def html_ip(request: Request):
    return f"<html><body>Your IP is: {request.client.host}</body></html>"

@app.get("/rooms")
def get_rooms():
    rooms = [
        {"name": "living room", "color": "blue", "floor": 1},
        {"name": "kitchen", "color": "red", "floor": 1},
        {"name": "bedroom", "color": "green", "floor": 2}
    ]
    return rooms                


#create booking route
@app.post("/bookings")
def create_booking():
    return {"msg": "Booking created successfully"}



    







