from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.db import get_conn, wait_for_db, create_schema

app = FastAPI()

# Wait for PostgreSQL and create tables
wait_for_db()
create_schema()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Booking(BaseModel):
    guest_id: int
    room_id: int


my_name = "Liza"


@app.get("/")
def read_root():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT 'hello postgres' AS message;")
        result = cur.fetchone()

    return {
        "msg": f"Hello, {my_name}",
        "db_status": result
    }


@app.get("/if/{term}")
def if_test(term: str):
    if term == "hello" or term == "hi":
        msg = "Hello yourself"
    elif term == "hej" or term == "moi":
        msg = "Hi in Swedish or Finnish"
    else:
        msg = f"I do not understand {term}"

    return {"msg": msg}


@app.get("/api/ip")
def api_ip(request: Request):
    return {"ip": request.client.host}


@app.get("/ip", response_class=HTMLResponse)
def html_ip(request: Request):
    return f"<html><body>Your IP is: {request.client.host}</body></html>"


@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, room_number, room_type, price, created_at
            FROM rooms
            ORDER BY id
        """)
        rooms = cur.fetchall()

    return rooms


#get one room 

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, room_number, room_type, price, created_at
            FROM rooms
            WHERE id = %s
        """, [room_id])

        room = cur.fetchone()

    if room is None:
        return {"error": "Room not found"}

    return room

@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO bookings (room_id, guest_id)
            VALUES (%s, %s)
            RETURNING id, room_id, guest_id, datefrom, dateto, info, created_at
        """, [booking.room_id, booking.guest_id])

        result = cur.fetchone()

    return {
        "msg": "Booking created successfully",
        "booking": result
    }


