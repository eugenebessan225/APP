CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS ml_table(
    predict_ID INTEGER,
    ope_ID INTEGER
    time timestamp,
    predict_value INTEGER,
    pred_eval INTEGER
);