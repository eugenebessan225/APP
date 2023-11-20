CREATE TABLE IF NOT EXISTS sensors_raw(
  time timestamp,
  acc_0 real,
  acc_1 real
  );

SELECT create_hypertable('sensors_raw', 'time', chunk_time_interval => INTERVAL '1 week');

CREATE TABLE IF NOT EXISTS sensors_rms(
  time timestamp,
  acc_0_rms real,
  acc_1_rms real
  );

SELECT create_hypertable('sensors_rms', 'time',  chunk_time_interval => INTERVAL '1 week');