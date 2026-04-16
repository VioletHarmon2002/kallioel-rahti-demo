import os, psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

def create_schema():
    with get_conn() as conn, conn.cursor() as cur:

        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id SERIAL PRIMARY KEY,
            room_number INTEGER NOT NULL,
            room_type VARCHAR,
            created_at TIMESTAMP NOT NULL DEFAULT now()
        );
        """)

        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS hotel_guests (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR NOT NULL,
            last_name VARCHAR NOT NULL,
            address VARCHAR NOT NULL
        );
        """)

        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS hotel_bookings (
            id SERIAL PRIMARY KEY,
            guest_key INTEGER REFERENCES hotel_guests(id),
            room_id INTEGER REFERENCES rooms(id),
            datefrom TIMESTAMP NOT NULL,
            dateto TIMESTAMP NOT NULL,
            add_info VARCHAR
        );
        """)