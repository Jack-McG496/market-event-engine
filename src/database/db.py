from sqlalchemy import create_engine, text
from contextlib import contextmanager

DB_URL = "postgresql://energy_user:energy_pass@localhost:5432/energy_market"

engine = create_engine(DB_URL, pool_pre_ping=True)


@contextmanager
def get_connection():
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()


# =========================
# INSERT FUNCTIONS
# =========================

def insert_event(event):
    query = text("""
        INSERT INTO events (
            event_type, event_time, asset,
            forecast, actual, previous, surprise, source
        )
        VALUES (
            :event_type, :event_time, :asset,
            :forecast, :actual, :previous, :surprise, :source
        )
        RETURNING id;
    """)

    with get_connection() as conn:
        result = conn.execute(query, event)
        conn.commit()
        return result.fetchone()[0]


def insert_event_analysis(analysis):
    query = text("""
        INSERT INTO event_analysis (
            event_id, bias, magnitude, time_horizon,
            confidence, explanation
        )
        VALUES (
            :event_id, :bias, :magnitude, :time_horizon,
            :confidence, :explanation
        );
    """)

    with get_connection() as conn:
        conn.execute(query, analysis)
        conn.commit()


def insert_market_price(price):
    query = text("""
        INSERT INTO market_prices (asset, timestamp, price)
        VALUES (:asset, :timestamp, :price);
    """)

    with get_connection() as conn:
        conn.execute(query, price)
        conn.commit()


def insert_event_reaction(reaction):
    query = text("""
        INSERT INTO event_reactions (
            event_id,
            price_at_release,
            price_1h,
            price_4h,
            price_24h,
            pct_move_1h,
            pct_move_4h,
            pct_move_24h
        )
        VALUES (
            :event_id,
            :price_at_release,
            :price_1h,
            :price_4h,
            :price_24h,
            :pct_move_1h,
            :pct_move_4h,
            :pct_move_24h
        );
    """)

    with get_connection() as conn:
        conn.execute(query, reaction)
        conn.commit()


# =========================
# QUERY FUNCTIONS
# =========================

def get_recent_events(limit=10):
    query = text("""
        SELECT *
        FROM events
        ORDER BY event_time DESC
        LIMIT :limit;
    """)

    with get_connection() as conn:
        result = conn.execute(query, {"limit": limit})
        return result.fetchall()


def get_event_with_analysis():
    query = text("""
        SELECT e.*, a.bias, a.magnitude, a.confidence
        FROM events e
        LEFT JOIN event_analysis a
        ON e.id = a.event_id
        ORDER BY e.event_time DESC;
    """)

    with get_connection() as conn:
        result = conn.execute(query)
        return result.fetchall()