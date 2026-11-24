
-- PHARMACEUTICAL SUPPLY CHAIN INTELLIGENCE
-- Database: pharma_intelligence

-- 1. PRODUCTS
CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    manufacturer VARCHAR(150) NOT NULL,
    category VARCHAR(80) NOT NULL
);

-- 2. BATCHES
CREATE TABLE batches (
    batch_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    manufacture_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),

    CONSTRAINT fk_batch_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT valid_batch_dates
        CHECK (expiry_date > manufacture_date),

    UNIQUE (batch_id, product_id)
);

-- 3. LOCATIONS
CREATE TABLE locations (
    location_id VARCHAR(20) PRIMARY KEY,
    location_name VARCHAR(150) NOT NULL,
    country VARCHAR(80) NOT NULL,
    location_type VARCHAR(50) NOT NULL
);

-- 4. VERIFICATION EVENTS
CREATE TABLE verification_events (
    event_id VARCHAR(30) PRIMARY KEY,
    serial_number VARCHAR(80) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    batch_id VARCHAR(20) NOT NULL,
    location_id VARCHAR(20) NOT NULL,
    event_timestamp TIMESTAMPTZ NOT NULL,

    verification_status VARCHAR(40) NOT NULL,
    response_reason VARCHAR(80) NOT NULL,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (batch_id, product_id)
        REFERENCES batches(batch_id, product_id),

    FOREIGN KEY (location_id)
        REFERENCES locations(location_id),

    CHECK (
        verification_status IN (
            'SUCCESS',
            'UNKNOWN_PRODUCT',
            'ALREADY_DECOMMISSIONED',
            'EXPIRED',
            'RECALLED'
        )
    )
);

-- 5. INDEXES FOR ANALYTICAL QUERIES

CREATE INDEX idx_events_serial
ON verification_events(serial_number);

CREATE INDEX idx_events_timestamp
ON verification_events(event_timestamp);

CREATE INDEX idx_events_status
ON verification_events(verification_status);

CREATE INDEX idx_events_location
ON verification_events(location_id);

CREATE INDEX idx_events_product
ON verification_events(product_id);
