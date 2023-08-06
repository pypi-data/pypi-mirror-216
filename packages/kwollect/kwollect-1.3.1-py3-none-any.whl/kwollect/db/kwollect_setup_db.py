#!/usr/bin/python3

import psycopg2
import jwt

from pyonf import pyonf

config = """
db_host: /var/run/postgresql/
db_port: 5432
db_admin: postgres
db_admin_password: changeme
kwollect_db_name: kwdb
kwollect_user: kwuser
kwollect_password: changeme
kwollect_password_ro: ro
chunk_interval_hour: 6
chunk_compress_hour: 24
request_timeout_min: 5
archive_path: ''
"""
config = pyonf(config, mandatory_opts=["kwollect_password"])
globals().update(config)

# We must set chunk_interval_hour so that data in most recent interval fits in memory
# 1 row is about 200 units of storage
# ie: chunk_time_interval (sec) = (0.25*mem_size_in_mbytes*10^6) / (num_metrics_per_second*200)
# For instance, a 8GB machine would handle a chunk of one day with 100 metrics per sec.


def sql(cmd):
    global sql_cur
    # print(cmd)
    sql_cur.execute(cmd)



sql_conn = psycopg2.connect(
    host=db_host, port=db_port, user=db_admin, password=db_admin_password
)
sql_conn.autocommit = True
sql_cur = sql_conn.cursor()

sql(f"SELECT * FROM pg_database WHERE datname = '{kwollect_db_name}'")
db_exists = False
try:
    if sql_cur.fetchall():
        db_exists = True
except psycopg2.ProgrammingError:
    pass

if db_exists:
    print(
        f"Database {kwollect_db_name} already exists, skipping database and users creation"
    )
else:
    print("Creating database...")
    sql(f"CREATE DATABASE {kwollect_db_name}")

    cmd = f"""
    DROP ROLE IF EXISTS {kwollect_user};
    CREATE USER {kwollect_user} WITH ENCRYPTED PASSWORD '{kwollect_password}';
    DROP ROLE IF EXISTS {kwollect_user}_ro;
    CREATE ROLE {kwollect_user}_ro WITH ENCRYPTED PASSWORD '{kwollect_password_ro}';
    GRANT ALL PRIVILEGES ON DATABASE {kwollect_db_name} TO {kwollect_user};
    GRANT {kwollect_user}_ro TO {kwollect_user};
    """
    sql(cmd)
cmd = f"""
ALTER USER {kwollect_user} WITH ENCRYPTED PASSWORD '{kwollect_password}';
ALTER USER {kwollect_user}_ro WITH ENCRYPTED PASSWORD '{kwollect_password_ro}';
ALTER USER {kwollect_user}_ro LOGIN;
ALTER DATABASE kwdb SET idle_in_transaction_session_timeout TO '1 h';
ALTER DATABASE kwdb SET statement_timeout TO '1 h';
ALTER ROLE {kwollect_user} SET statement_timeout TO '{int(request_timeout_min)} min';
"""
sql(cmd)

sql_conn = psycopg2.connect(
    dbname=kwollect_db_name,
    host=db_host,
    port=db_port,
    user=db_admin,
    password=db_admin_password,
)
sql_conn.autocommit = True
sql_cur = sql_conn.cursor()

print("Creating or updating database schema...")
cmd = f"""
SET LOCAL SESSION AUTHORIZATION DEFAULT;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE EXTENSION IF NOT EXISTS timescaledb_toolkit;

SET LOCAL SESSION AUTHORIZATION {kwollect_user};

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO {kwollect_user}_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA _timescaledb_internal GRANT SELECT ON TABLES TO {kwollect_user}_ro;

CREATE TABLE IF NOT EXISTS metrics (
  timestamp   TIMESTAMPTZ       DEFAULT NOW(),
  device_id   TEXT              NOT NULL,
  metric_id   TEXT              NOT NULL,
  value       DOUBLE PRECISION  DEFAULT 'NaN',
  labels      JSONB             DEFAULT  '{{}}'::JSONB
  );

SELECT create_hypertable('metrics', 'timestamp', chunk_time_interval => INTERVAL '{chunk_interval_hour} hours', if_not_exists => true);
SELECT set_chunk_time_interval('metrics', INTERVAL '{chunk_interval_hour} hours');

DO $$
BEGIN
  BEGIN ALTER TABLE metrics SET (
      timescaledb.compress,
      timescaledb.compress_segmentby = 'device_id, metric_id, labels',
      timescaledb.compress_orderby = 'timestamp DESC'
      );
  EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Compression already enabled';
  END;
END $$;
SELECT add_compression_policy('metrics', INTERVAL '{chunk_compress_hour} hours', if_not_exists => true);

CREATE INDEX IF NOT EXISTS metrics_device_idx ON metrics(device_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS metrics_alias_idx
  ON metrics((labels->>'_device_alias'), timestamp DESC)
  WHERE labels ? '_device_alias';

CREATE TABLE IF NOT EXISTS promoted_metrics (
  device_id   TEXT              NOT NULL,
  metric_id   TEXT              DEFAULT NULL
  );

CREATE OR REPLACE VIEW nodetime_by_job AS
  SELECT * FROM
    (SELECT 0 AS job_id, now() AS start_time, now() AS stop_time, '' AS node) empty
  WHERE false;

CREATE MATERIALIZED VIEW IF NOT EXISTS metrics_summary
  WITH (timescaledb.continuous) AS
  SELECT time_bucket(INTERVAL '5 minute', timestamp) AS timestamp,
    device_id,
    metric_id,
    CASE WHEN metrics.metric_id ~ '_total$' THEN MAX(value) ELSE AVG(value) END AS value,
    labels - '_metric_scrape_time' AS labels
  FROM metrics
  GROUP BY time_bucket(INTERVAL '5 minute', timestamp), device_id, metric_id, labels - '_metric_scrape_time'
  WITH NO DATA;

SELECT add_continuous_aggregate_policy('metrics_summary',
    start_offset => INTERVAL '12 hour',
    end_offset => INTERVAL '10 minute',
    schedule_interval => INTERVAL '5 minute',
    if_not_exists => true);

DO $$
BEGIN
  BEGIN ALTER MATERIALIZED VIEW metrics_summary SET (
      timescaledb.compress
      );
  EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Compression already enabled';
  END;
END $$;
SELECT add_compression_policy('metrics_summary', INTERVAL '2 day', if_not_exists => true);

"""
sql(cmd)

for suffix in ['', '_summary']:
  cmd = f"""
SET LOCAL SESSION AUTHORIZATION {kwollect_user};
CREATE OR REPLACE VIEW metrics_by_device{suffix} AS
 SELECT metrics."timestamp",
    metrics.device_id,
    metrics.metric_id,
    metrics.value,
    metrics.labels - '_device_alias' AS labels
   FROM metrics{suffix} AS metrics
UNION ALL (
  SELECT metrics."timestamp",
    metrics.labels ->> '_device_alias'::text AS device_id,
    metrics.metric_id,
    sum(metrics.value) AS value,
    (metrics.labels || jsonb_build_object('_device_orig', array_agg(metrics.device_id ORDER BY metrics.device_id))) - '_device_alias' AS labels
   FROM metrics{suffix} AS metrics
  WHERE metrics.labels ? '_device_alias'::text
  GROUP BY metrics."timestamp", metrics.metric_id, metrics.labels
);

CREATE OR REPLACE VIEW metrics_by_job{suffix} AS
 SELECT nodemetrics."timestamp",
    nodemetrics.device_id,
    nodemetrics.metric_id,
    nodemetrics.value,
    nodemetrics.labels,
    nodetime.start_time,
    nodetime.stop_time,
    nodetime.job_id
   FROM (
     SELECT nodetime_by_job.job_id,
            nodetime_by_job.node,
            nodetime_by_job.start_time,
            nodetime_by_job.stop_time
     FROM nodetime_by_job
     ) nodetime
   JOIN LATERAL (
     SELECT metrics."timestamp",
            metrics.device_id,
            metrics.metric_id,
            metrics.value,
            metrics.labels - '_device_alias' AS labels
     FROM metrics{suffix} AS metrics
     WHERE metrics."timestamp" > nodetime.start_time
       AND (nodetime.stop_time IS NULL OR metrics."timestamp" < nodetime.stop_time)
       AND metrics.device_id = nodetime.node
     UNION ALL
     SELECT metrics."timestamp",
            metrics.labels ->> '_device_alias'::text AS device_id,
            metrics.metric_id,
            sum(metrics.value) AS value,
            (metrics.labels || jsonb_build_object('_device_orig', array_agg(metrics.device_id))) - '_device_alias'
     FROM metrics{suffix} AS metrics
     WHERE metrics.labels ? '_device_alias'::text
       AND metrics.labels ->> '_device_alias' = nodetime.node
       AND metrics."timestamp" > nodetime.start_time
       AND (nodetime.stop_time IS NULL OR metrics."timestamp" < nodetime.stop_time)
     GROUP BY metrics."timestamp", metrics.metric_id, metrics.labels
     ) nodemetrics ON true;

"""
  sql(cmd)

if archive_path:

    sql(f"SELECT 1 FROM pg_tablespace WHERE spcname = 'archive';")
    ts_exists = False
    try:
        if sql_cur.fetchall():
            ts_exists = True
    except psycopg2.ProgrammingError:
        pass
    if not ts_exists:
        cmd=f"CREATE TABLESPACE archive OWNER {kwollect_user} LOCATION '{archive_path}';"
        sql(cmd)

    cmd="""
SET LOCAL SESSION AUTHORIZATION DEFAULT;

CREATE OR REPLACE PROCEDURE move_chunks_to_archive (job_id int, config jsonb)
LANGUAGE PLPGSQL
AS $$
DECLARE
  ht REGCLASS;
  lag interval;
  destination name;
  chunk REGCLASS;
  tmp_name name;
BEGIN
  SELECT jsonb_object_field_text (config, 'hypertable')::regclass INTO STRICT ht;
  SELECT jsonb_object_field_text (config, 'lag')::interval INTO STRICT lag;
  SELECT jsonb_object_field_text (config, 'tablespace') INTO STRICT destination;

  IF ht IS NULL OR lag IS NULL OR destination IS NULL THEN
    RAISE EXCEPTION 'Config must have hypertable, lag and destination';
  END IF;

  RAISE LOG 'Checking for chunks to archive in: %', ht::text;

  FOR chunk IN
  SELECT sc
  FROM
    show_chunks(ht, older_than => lag) sc,
    timescaledb_information.chunks tsi
  WHERE
    sc::text=CONCAT(tsi.chunk_schema, '.', tsi.chunk_name) AND
    (tsi.chunk_tablespace IS NULL OR tsi.chunk_tablespace != destination)
  LOOP
    RAISE LOG 'Moving chunk: %', chunk::text;
    EXECUTE format('
      SELECT move_chunk(
        chunk => ''%s'',
        destination_tablespace => ''%I'',
        index_destination_tablespace => ''%I''
      )', chunk, destination, destination);
  END LOOP;
END
$$;

DO $$
  DECLARE j record;
BEGIN
  FOR j IN SELECT job_id FROM timescaledb_information.jobs WHERE proc_name = 'move_chunks_to_archive'
    LOOP PERFORM delete_job(j.job_id);
  END LOOP;
END
$$;
SELECT add_job(
  'move_chunks_to_archive', '1d',
  config => '{"hypertable":"metrics_summary", "lag":"8d", "tablespace":"archive"}',
  initial_start => CURRENT_DATE + TIME '23:59:59' AT TIME ZONE current_setting('TIMEZONE')
  );
"""
    sql(cmd)

cmd = f"""
SET LOCAL SESSION AUTHORIZATION default;
CREATE SCHEMA IF NOT EXISTS api;
GRANT ALL PRIVILEGES ON SCHEMA api TO {kwollect_user};
GRANT USAGE ON SCHEMA api TO {kwollect_user}_ro;

CREATE EXTENSION IF NOT EXISTS plpython3u;
UPDATE pg_language SET lanpltrusted = true WHERE lanname = 'plpython3u';


SET LOCAL SESSION AUTHORIZATION {kwollect_user};

DROP FUNCTION IF EXISTS api.get_metrics;
CREATE OR REPLACE FUNCTION api.get_metrics(job_id INTEGER DEFAULT NULL,
                                           nodes TEXT DEFAULT NULL,
                                           devices TEXT DEFAULT NULL,
                                           metrics TEXT DEFAULT NULL,
                                           start_time TEXT DEFAULT NULL,
                                           end_time TEXT DEFAULT NULL,
                                           summary BOOLEAN DEFAULT FALSE,
                                           as_rate BOOLEAN DEFAULT FALSE)
RETURNS SETOF metrics AS $$
from plpy import spiexceptions

def time_to_sql(time):
    if not time:
        time = "now"
    try:
        return "to_timestamp(%f)" % float(time)
    except ValueError:
        return "'%s'::timestamp with time zone" % time

global start_time, end_time

_devices = ",".join([arg for arg in [nodes,devices] if arg])

if not job_id and not _devices:
    plpy.error("Missing 'devices', 'nodes' or 'job_id' argument")

if job_id:
    nodetime = plpy.execute("SELECT MIN(start_time) AS start_time, COALESCE(MAX(stop_time), NOW()) AS stop_time, STRING_AGG(node, ',') AS nodes FROM nodetime_by_job WHERE job_id = %s GROUP BY job_id" % job_id)[0]
    if not start_time:
        start_time = nodetime["start_time"]
    # TODO Fix for running job
    if not end_time:
        end_time = nodetime["stop_time"]
    if not _devices:
        _devices = nodetime["nodes"]

suffix = ""
if summary:
    suffix = "_summary"

cond = []
req = "SELECT * FROM metrics_by_device%s WHERE " % suffix

if _devices:
    _devices = [device.split('.')[0] for device in _devices.split(",")]
    cond.append("device_id in ('%s')" % "','".join(_devices))

if start_time and end_time:
    start_time_sql = time_to_sql(start_time)
    end_time_sql = time_to_sql(end_time)
elif start_time and not end_time:
    start_time_sql = time_to_sql(start_time)
    end_time_sql = time_to_sql(plpy.execute("SELECT %s + INTERVAL '5min' AS t" % start_time_sql)[0]["t"])
elif not start_time and end_time:
    end_time_sql = time_to_sql(end_time)
    start_time_sql = time_to_sql(plpy.execute("SELECT %s - INTERVAL '5min' AS t" % end_time_sql)[0]["t"])
else:
    end_time_sql = time_to_sql(plpy.execute("SELECT NOW() AS t")[0]["t"])
    start_time_sql = time_to_sql(plpy.execute("SELECT %s - INTERVAL '5min' AS t" % end_time_sql)[0]["t"])
cond.append("timestamp >= %s AND timestamp <= %s" % (start_time_sql, end_time_sql))

if metrics:
    metrics_id = metrics.split(",")
    cond.append("metric_id in ('%s')" % "','".join(metrics_id))

req += " AND ".join(cond)
req += " ORDER BY timestamp ASC"

if as_rate:
    req = "WITH cte AS (%s)" % req
    req += "\\n" \
"SELECT " \
  "timestamp, device_id, metric_id, " \
  "CASE WHEN timestamp = LAG(timestamp) OVER w THEN NULL " \
     "WHEN LAG(value) OVER w IS NULL THEN NULL " \
     "WHEN value < LAG(value) OVER w THEN MAX(value) OVER w - LAG(value) OVER w + value " \
     "ELSE (value - LAG(value) OVER w) " \
  "END / EXTRACT(epoch FROM timestamp - LAG(timestamp) OVER w) AS value, " \
  "labels " \
"FROM cte " \
"WINDOW w AS (PARTITION BY metric_id, device_id, labels ORDER BY timestamp ASC) "\
"ORDER BY timestamp ASC"

plpy.info(req)
try:
    return plpy.execute(req)
except spiexceptions.QueryCanceled:
    raise Exception("Request timeout, too much data to process.")

$$ LANGUAGE 'plpython3u' IMMUTABLE;


DROP FUNCTION IF EXISTS api.available_metrics;
CREATE OR REPLACE FUNCTION api.available_metrics(
  at          TIMESTAMPTZ       DEFAULT NOW(),
  params      JSONB             DEFAULT '{{}}'
)
RETURNS TABLE (device_id TEXT, metric_id TEXT) AS $$
DECLARE
from_devices    TEXT[]    := NULL;
from_job_id     INT       := NULL;
from_job_id_end TIMESTAMP := NULL;
BEGIN
IF params->>'job_id' IS NOT NULL THEN
  SELECT nullif(substring(params->>'job_id' FROM '^\d+$'), '')::int INTO from_job_id;
  IF from_job_id IS NOT NULL THEN
    SELECT COALESCE(MAX(stop_time), NOW()) FROM nodetime_by_job WHERE job_id = from_job_id INTO from_job_id_end;
    SELECT ARRAY(SELECT DISTINCT node FROM nodetime_by_job WHERE nodetime_by_job.job_id = from_job_id) INTO from_devices;
    RETURN QUERY SELECT * FROM api.available_metrics(at => LEAST(from_job_id_end, at), params => jsonb_build_object('devices', array_to_json(from_devices)));
    RETURN;
  END IF;
END IF;
IF params->'devices' IS NOT NULL THEN
  IF jsonb_typeof(params->'devices') = 'array' THEN
    SELECT ARRAY(SELECT jsonb_array_elements_text(params->'devices')) INTO STRICT from_devices;
  ELSE
    RAISE EXCEPTION 'Cannot parse params->devices, should be JSON array';
  END IF;
END IF;
RETURN QUERY
WITH av_metrics AS (
  SELECT metrics.device_id, metrics.metric_id
  FROM metrics AS metrics WHERE
  timestamp < at AND timestamp > at - INTERVAL '1m'
  AND CASE WHEN from_devices IS NOT NULL THEN metrics.device_id = ANY (from_devices) ELSE true END
  UNION
  SELECT metrics.labels ->> '_device_alias'::text AS device_id, metrics.metric_id
  FROM metrics AS metrics
  WHERE metrics.labels ? '_device_alias'
  AND timestamp < at AND timestamp > at - INTERVAL '1m'
  AND CASE WHEN from_devices IS NOT NULL THEN metrics.labels->>'_device_alias' = ANY (from_devices) ELSE true END
),
ordered_metrics AS (
  SELECT DISTINCT ON (idx1, idx2, idx3, metric_id)
    metrics.device_id, metrics.metric_id,
    CASE WHEN metrics.device_id ~ '^[a-z]+-\d+$' THEN '1' ELSE '2' END AS idx1,
    (STRING_TO_ARRAY(metrics.device_id, '-'))[1] AS idx2,
    COALESCE(SUBSTRING((STRING_TO_ARRAY(metrics.device_id, '-'))[2] FROM '([0-9]+)')::INTEGER, 0) as idx3
  FROM av_metrics AS metrics
  ORDER BY idx1, idx2, idx3, metric_id
)
SELECT m.device_id, m.metric_id FROM ordered_metrics AS m;
END;
$$ LANGUAGE plpgsql IMMUTABLE;


CREATE OR REPLACE FUNCTION api.insert_metrics(
  device_id   TEXT,
  metric_id   TEXT,
  "timestamp" TIMESTAMPTZ       DEFAULT NOW(),
  value       DOUBLE PRECISION  DEFAULT 'NaN',
  labels      JSONB             DEFAULT  '{{}}'::JSONB
)
RETURNS SETOF metrics AS $$
BEGIN
  RETURN QUERY
    INSERT INTO metrics(timestamp, device_id, metric_id, value, labels)
      VALUES (timestamp, device_id, metric_id, value, labels)
    RETURNING *;
END;
$$ LANGUAGE 'plpgsql';
"""
sql(cmd)
print("Database setup done.")
print("")

jwtsecret = kwollect_password * (1+(32//len(kwollect_password)))

print("Postgrest configuration file:")
print("-----------------")
print(
    f"""db-uri = "postgres://{kwollect_user}:{kwollect_password}@{db_host if not "/" in db_host else "localhost"}:{db_port}/{kwollect_db_name}"
db-schema = "api"
db-anon-role = "{kwollect_user}_ro"
jwt-secret = "{jwtsecret}" """
)
print("-----------------")
print("")
print("API token:")
print("-----------------")
print(
    jwt.encode(
        {"role": kwollect_user}, jwtsecret, algorithm="HS256"
    )
)
print("-----------------")


def main():
    pass
if __name__ == "__main__":
    main()
