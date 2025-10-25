-- Economic Intelligence System Database Tables

-- Gold and Silver Prices Table
CREATE TABLE IF NOT EXISTS gold_silver_prices (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    gold_price_usd DECIMAL(10,2),
    silver_price_usd DECIMAL(10,2),
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- USD/EGP Exchange Rates Table
CREATE TABLE IF NOT EXISTS usd_egp_rates (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    usd_egp_rate DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);




