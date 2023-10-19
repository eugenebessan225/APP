CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS hyperparams_raw(
    program_ID INTEGER,
    op_type TEXT,
    materiaux TEXT,
    speed_f REAL,
    seep_r REAL,
    outillage TEXT,
    metadata JSONB
);