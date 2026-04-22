import os
import time
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg.connect(
        DATABASE_URL,
        autocommit=True,
        row_factory=dict_row
    )


def wait_for_db(max_retries=10, delay=2):
    for attempt in range(max_retries):
        try:
            with get_conn() as conn:
                print("Database is ready.")
                return
        except psycopg.OperationalError as e:
            print(f"Database not ready yet ({attempt + 1}/{max_retries}): {e}")
            time.sleep(delay)

    raise Exception("Database did not become ready in time.")


def create_schema():
    with get_conn() as conn, conn.cursor() as cur:
        # Create the schema
        cur.execute("""
            -- Add pgcrypto
            CREATE EXTENSION IF NOT EXISTS pgcrypto;
                    
            ----------
            -- ROOMS
            ----------
            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                room_number INT NOT NULL,
                created_at TIMESTAMP DEFAULT now()
            );
                    
            -- add columns
            ALTER TABLE rooms ADD COLUMN IF NOT EXISTS room_type VARCHAR;
            ALTER TABLE rooms ADD COLUMN IF NOT EXISTS price NUMERIC NOT NULL DEFAULT 0;

            ----------
            -- Guests
            ----------
            CREATE TABLE IF NOT EXISTS guests (
                id SERIAL PRIMARY KEY,
                firstname VARCHAR NOT NULL,
                lastname VARCHAR NOT NULL,
                address VARCHAR,
                created_at TIMESTAMP DEFAULT now()
            );
            ALTER TABLE guests ADD COLUMN IF NOT EXISTS api_key VARCHAR DEFAULT encode(gen_random_bytes(32), 'hex');

            ----------
            -- Bookings
            ----------
            CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            guest_id INT REFERENCES guests(id),
            room_id INT REFERENCES rooms(id),
            datefrom DATE NOT NULL DEFAULT CURRENT_DATE,
            dateto DATE NOT NULL DEFAULT (CURRENT_DATE + 1),
            info VARCHAR,
            created_at TIMESTAMP DEFAULT now()
);

ALTER TABLE bookings
ALTER COLUMN dateto SET DEFAULT (CURRENT_DATE + 1);


        """)