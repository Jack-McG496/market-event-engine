from sqlalchemy import create_engine, text

DB_URL = "postgresql://energy_user:energy_pass@localhost:5432/energy_market"

def init_db():
    engine = create_engine(DB_URL)

    with open("src/database/events_schema.sql", "r") as f:
        schema_sql = f.read()

    with engine.connect() as conn:
        conn.execute(text(schema_sql))
        conn.commit()

    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()