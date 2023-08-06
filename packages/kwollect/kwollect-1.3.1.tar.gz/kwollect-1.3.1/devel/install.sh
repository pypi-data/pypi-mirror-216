#!/bin/bash

set -x
set -e

# Req
apt update
apt install -y --no-install-recommends wget gnupg hwloc xz-utils ca-certificates


# Kwollect
# echo 'deb [trusted=yes] http://packages.grid5000.fr/deb/kwollect /' > /etc/apt/sources.list.d/kwollect.list
# apt update
# apt install -y kwollect
apt install -y --no-install-recommends python3-pip python3-setuptools python3-yarl
pip3 install -U pip
pip3 install -e /vagrant
cat /vagrant/debian/kwollector.service | sed 's,bin/kwollector,local/bin/kwollector,g' > /etc/systemd/system/kwollector.service

# Database
pg_dropcluster --stop 13 main || true
pg_createcluster 13 main
systemctl restart postgresql

wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | apt-key add -
echo 'deb https://packagecloud.io/timescale/timescaledb/debian/ bullseye main' > /etc/apt/sources.list.d/timescaledb.list
apt update
apt-get install -y --no-install-recommends postgresql postgresql-client libpq-dev timescaledb-2-postgresql-13 timescaledb-toolkit-postgresql-13 timescaledb-tools postgresql-plpython3-13

## TimescaleDB comes with a script to tune Postgres configuration that you might want to use:
cp /etc/postgresql/13/main/postgresql.conf /etc/postgresql/13/main/postgresql.conf-timescaledb_tune.backup
timescaledb-tune -yes -quiet
echo 'timescaledb.telemetry_level=off' >> /etc/postgresql/13/main/postgresql.conf

sed -i 's/max_connections.*/max_connections = 1000/g' /etc/postgresql/13/main/postgresql.conf

systemctl restart postgresql

# API
[ -f /tmp/postgrest.txz ] || wget -q -O /tmp/postgrest.txz https://github.com/PostgREST/postgrest/releases/download/v10.1.2/postgrest-v10.1.2-linux-static-x64.tar.xz
cd /tmp
tar xf postgrest.txz
chmod +x ./postgrest
mv ./postgrest /usr/local/bin/

cat > /etc/postgrest.conf << EOF
db-uri = "postgres://kwuser:changeme@localhost/kwdb"
db-schema = "api"
db-anon-role = "kwuser_ro"
jwt-secret = "changemechangemechangemechangemechangeme"
EOF

cat > /etc/systemd/system/postgrest.service << EOF
[Unit]
Description=Postgrest service
After=network.target

[Service]
ExecStart=/usr/local/bin/postgrest /etc/postgrest.conf

[Install]
WantedBy=multi-user.target
EOF

systemctl enable postgrest

# Kwollector
mkdir -p /etc/kwollect/metrics.d
cat > /etc/kwollect/kwollector.conf << EOF
# Path to directory containing metrics description
metrics_dir: /etc/kwollect/metrics.d/

# Hostname of postgresql server
db_host: localhost

# Database name
db_name: kwdb

# Database user
db_user: kwuser

# Database password
db_password: changeme

# Log level
log_level: warning
EOF
cat > /etc/kwollect/metrics.d/metrics.yaml << EOF
- name: snmp_dumb
  device_id: local
  url: snmp://public@127.0.0.1/1.3.6.1.2.1.25.1.7.0
  update_every: 5000

- name: snmp_template
  device_id: local
  url: snmp://public@127.0.0.1/1.3.6.1.2.1.1.9.1.4.{{ 1.3.6.1.2.1.1.9.1.3 == The SNMP Management Architecture MIB. }}
  update_every: 5000

- name: prom_default_metric
  device_id: local
  url: prometheus://localhost:9100/node_load1-node_load5-node_load15-node_cpu_total
  update_every: 15000

- name: prom_all_metrics
  device_id: local
  url: prometheus://localhost:9100/
  update_every: 15000
  optional: true
EOF

apt install -y --no-install-recommends prometheus-node-exporter snmpd
systemctl enable kwollector


# Grafana


apt-get install -y --no-install-recommends apt-transport-https software-properties-common wget
wget -q -O /usr/share/keyrings/grafana.key https://apt.grafana.com/gpg.key
echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://apt.grafana.com stable main" > /etc/apt/sources.list.d/grafana.list
apt-get update
apt-get install grafana

sed -i 's/.*http_port.*/http_port = 3003/g' /etc/grafana/grafana.ini
cp /vagrant/kwollect/grafana/postgres_datasource.yaml /etc/grafana/provisioning/datasources/postgres.yaml
cp /vagrant/kwollect/grafana/kwollect_dashboardsource.yaml /etc/grafana/provisioning/dashboards/kwollect.yaml
mkdir -p /etc/grafana/kwollect_dashboard
ln -sf /vagrant/kwollect/grafana/kwollect_dashboard.json /etc/grafana/kwollect_dashboard/

systemctl start grafana-server
systemctl enable grafana-server
