CREATE DATABASE eis_db;

\c eis_db

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

-- Economic Indicators Table
CREATE TABLE IF NOT EXISTS economic_indicators (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    inflation_rate DECIMAL(10,4),
    gdp_growth_rate DECIMAL(10,4),
    unemployment_rate DECIMAL(10,4),
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

