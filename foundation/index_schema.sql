
-- Affiliate Programs Schema
CREATE TABLE affiliate_networks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    api_endpoint VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE affiliate_programs (
    id SERIAL PRIMARY KEY,
    network_id INTEGER REFERENCES affiliate_networks(id),
    program_id VARCHAR(100),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    commission_type VARCHAR(50),
    commission_rate DECIMAL(10,2),
    cookie_duration INTEGER,
    region VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE program_metrics (
    id SERIAL PRIMARY KEY,
    program_id INTEGER REFERENCES affiliate_programs(id),
    epc DECIMAL(10,2),
    conversion_rate DECIMAL(5,2),
    average_order_value DECIMAL(10,2),
    total_sales INTEGER,
    measurement_period VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_program_category ON affiliate_programs(category);
CREATE INDEX idx_program_region ON affiliate_programs(region);
CREATE INDEX idx_program_status ON affiliate_programs(status);
