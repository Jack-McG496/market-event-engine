-- =========================
-- EVENTS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    event_time TIMESTAMP NOT NULL,
    asset TEXT DEFAULT 'WTI',

    forecast DOUBLE PRECISION,
    actual DOUBLE PRECISION,
    previous DOUBLE PRECISION,
    surprise DOUBLE PRECISION,

    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- LLM ANALYSIS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS event_analysis (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id) ON DELETE CASCADE,

    bias TEXT,                -- bullish / bearish / neutral
    magnitude TEXT,           -- low / medium / high
    time_horizon TEXT,        -- intraday / short-term / medium-term
    confidence DOUBLE PRECISION,

    explanation TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- MARKET PRICES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS market_prices (
    id SERIAL PRIMARY KEY,
    asset TEXT NOT NULL,      -- WTI, BRENT, DXY
    timestamp TIMESTAMP NOT NULL,
    price DOUBLE PRECISION NOT NULL
);

-- =========================
-- EVENT REACTIONS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS event_reactions (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id) ON DELETE CASCADE,

    price_at_release DOUBLE PRECISION,
    price_1h DOUBLE PRECISION,
    price_4h DOUBLE PRECISION,
    price_24h DOUBLE PRECISION,

    pct_move_1h DOUBLE PRECISION,
    pct_move_4h DOUBLE PRECISION,
    pct_move_24h DOUBLE PRECISION,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- INDEXES (IMPORTANT)
-- =========================

CREATE INDEX IF NOT EXISTS idx_events_time ON events(event_time);
CREATE INDEX IF NOT EXISTS idx_prices_time ON market_prices(timestamp);
CREATE INDEX IF NOT EXISTS idx_prices_asset ON market_prices(asset);
CREATE INDEX IF NOT EXISTS idx_analysis_event_id ON event_analysis(event_id);
CREATE INDEX IF NOT EXISTS idx_reactions_event_id ON event_reactions(event_id);