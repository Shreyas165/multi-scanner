CREATE TABLE scans (
    id SERIAL PRIMARY KEY,
    scanner VARCHAR(10),
    data JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);