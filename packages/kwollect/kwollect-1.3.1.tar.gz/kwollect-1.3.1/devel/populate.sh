#!/bin/bash

set -x
set -e

#systemctl stop systemd-timesyncd.service
#date -s '2021-01-01 00:00:01'

### /!\ Remove PRIMARY KEY for fastest ingestion
#perl -0777 -i.original -pe 's/,\n +PRIMARY KEY\(timestamp, device_id, metric_id, labels\)//igs' /opt/kwollect/lib/python3.7/site-packages/kwollect/tools/kwollect_setup_db.py

mkdir -p /var/lib/dbarchive
chown postgres:postgres /var/lib/dbarchive
su postgres -s /bin/sh -c "kwollect-setup-db --chunk_interval_hour 1 --kwollect_password changeme --chunk_compress_hour $((24*365*10)) --request_timeout_min $((5*60)) --archive_path /var/lib/dbarchive"

## Populate DB
worker=$(hwloc-info | grep Core | awk '{print $3}')
num_devices=1000
num_metrics=100
metric_period=5
num_hours=$((24*2))
if [ -n "$1" ]; then
  num_hours=$1
fi
if [ -n "$2" ]; then
  num_devices=$2
fi
if [ -n "$3" ]; then
  num_metrics=$3
fi

#time_end=$(($(date +%s)/$metric_period*$metric_period))
time_end=$(date -d"1/1/2021" +%s)
time_start=$(($time_end - $num_hours*3600))
set +e
set +x
echo "Inserting $(printf %.2e $(($num_devices*$num_metrics*($time_end - $time_start)/($metric_period)))) lines"
for time_cur in $(seq $time_start $metric_period $time_end); do
  ((i=i%$worker)); ((i++==0)) && wait
  date_cur=$(date -d@$time_cur --rfc-3339=second)
  for metric_id in $(seq $num_metrics); do
    for device_id in $(seq $num_devices); do
      echo "$date_cur;device-$device_id;metric-$metric_id;$((42+$metric_id));\"{\"\"key\"\": \"\"value\"\", \"\"_device_alias\"\":\"\"node-$device_id\"\"}\""
    done
  done &
done | timescaledb-parallel-copy --reporting-period 10s --split ';' --db-name kwdb --table metrics --workers $worker --connection "host=localhost user=kwuser password=changeme"

set -e
set -x

# Compress half of the table
su postgres -c "echo \"WITH chunks AS (SELECT show_chunks('metrics') LIMIT (SELECT COUNT(*) FROM (SELECT show_chunks('metrics')) s)/2) SELECT compress_chunk(show_chunks, if_not_compressed => TRUE) FROM chunks;\" | psql kwdb"

# Fake Job scheduler database
echo "CREATE OR REPLACE VIEW nodetime_by_job AS
  SELECT 1 AS job_id, '2020-12-31 22:00:00+00'::timestamp with time zone as start_time, '2020-12-31 23:00:00+00'::timestamp with time zone as stop_time, 'device-1' as node UNION
  SELECT 1 AS job_id, '2020-12-31 22:00:00+00'::timestamp with time zone as start_time, '2020-12-31 23:00:00+00'::timestamp with time zone as stop_time, 'device-2' as node UNION
  SELECT 2 AS job_id, '2020-12-31 22:00:00+00'::timestamp with time zone as start_time, NULL::timestamp with time zone as stop_time, 'device-5' as node UNION
  SELECT 2 AS job_id, '2020-12-31 22:00:00+00'::timestamp with time zone as start_time, NULL::timestamp with time zone as stop_time, 'device-6' as node UNION
  SELECT 2 AS job_id, '2020-12-31 22:00:00+00'::timestamp with time zone as start_time, NULL::timestamp with time zone as stop_time, 'device-7' as node UNION
  SELECT 2 AS job_id, '2020-12-31 22:00:00+00'::timestamp with time zone as start_time, NULL::timestamp with time zone as stop_time, 'device-8' as node UNION
  SELECT 2 AS job_id, '2020-12-31 22:00:00+00'::timestamp with time zone as start_time, NULL::timestamp with time zone as stop_time, 'device-9' as node UNION
  SELECT 3 AS job_id, '2020-01-01 00:01:00+00'::timestamp with time zone as start_time, NULL::timestamp with time zone as stop_time, 'local' as node;" | su postgres -c "psql kwdb"

su postgres -s /bin/sh -c "echo \"CALL refresh_continuous_aggregate('metrics_summary', '2021-01-01 00:00:00'::timestamp with time zone - interval '1 day', NULL);\" | psql kwdb"
su postgres -s /bin/sh -c "echo ANALYSE metrics | psql kwdb"

systemctl restart postgrest kwollector
