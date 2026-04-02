from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()
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






