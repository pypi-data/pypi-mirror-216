#!/usr/bin/python3

import sys
import time
import re
import random
import asyncio
import concurrent
import glob
import traceback
import subprocess
import functools
import logging as log

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse, unquote

import yaml
import asyncpg
import aiosnmp
import aiohttp
from pyonf import pyonf

try:
    from orjson import dumps

    json_dumps = lambda x: dumps(x).decode()
except ImportError:
    from json import dumps as json_dumps


config = """
metrics_dir: /etc/kwollect/metrics.d/
db_host: localhost
db_name: kwdb
db_user: kwuser
db_password: changeme
log_level: warning
worker: 8
"""
config = pyonf(config)

log.basicConfig(
    level=str.upper(config.get("log_level", "warning")),
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)


def main():
    asyncio.run(async_main(), debug=config.get("log_level") == "debug")


async def async_main():

    await init_http()
    await init_psql()
    init_ipmi()

    metrics = load_metric_descriptions(config["metrics_dir"])
    metrics_per_device = merge_metrics_per_device_and_protocol(metrics)

    for device, metrics in metrics_per_device.items():

        req_interval_ms = min(metric.update_every for metric in metrics)
        log.info(
            "Scheduling %s requests every %s milli-seconds", device, req_interval_ms
        )
        asyncio.create_task(
            schedule_every(
                req_interval_ms / 1000,
                process_host_metrics,
                (device, metrics),
                task_name=f"{device.protocol}{device.port or ''}@{device.hostname}",
            )
        )

    log.info("Scheduling SNMP template parsing every 5 minutes")
    asyncio.create_task(
        schedule_every(
            300,
            parse_metrics_template,
            (metrics_per_device,),
            task_name=f"snmp_parse",
            delayed_start=0,
        )
    )

    sql_worker_count = config["worker"]
    log.info("Scheduling %s SQL workers every seconds", sql_worker_count)
    for i in range(sql_worker_count):
        asyncio.create_task(
            schedule_every(
                1,
                insert_metrics_values,
                task_name=f"sqlworker{i}",
                delayed_start=i / sql_worker_count,
                timeout_max_count=30,
            )
        )

    # Waiting for infinity, but catching failing tasks
    ended_task, _ = await asyncio.wait(
        asyncio.all_tasks(), return_when=asyncio.FIRST_COMPLETED
    )
    log.critical("Scheduler task %s as ended, that should not happen", ended_task)
    sys.exit(1)


@dataclass(frozen=True)
class MetricDevice:
    """A device to be queried by some protocol"""

    hostname: str
    protocol: str
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class MetricDescription:
    """A metrics to fetch"""

    name: str
    device_id: str
    url: str
    path: str = ""
    update_every: int = 10000
    optional: bool = False
    labels: dict = field(default_factory=dict)
    scale_factor: Optional[float] = None
    path_template: Optional[str] = None

    def __post_init__(self):
        _url = urlparse(self.url)
        self.device = MetricDevice(
            hostname=_url.hostname,
            protocol=_url.scheme,
            port=_url.port,
            username=unquote(_url.username) if _url.username else None,
            password=unquote(_url.password) if _url.password else None,
        )
        if _url.path:
            self.path = re.sub(r"^/", "", unquote(_url.path))

        if self.path and self.parse_template(self.path):
            self.path_template = self.path
            self.path = None

    def parse_template(self, path=None):
        if not path:
            path = self.path_template
        if path:
            m = re.findall(r"{{(.*)==(.*)}}", path)
            if m:
                return m[0][0].strip(), m[0][1].strip()
            else:
                return None


def load_metric_descriptions(metrics_dir):
    """Load metric descriptions from directory"""
    log.debug("Loading metric descriptions from %s", metrics_dir)
    metrics = []
    for description_file in glob.glob(metrics_dir + "/*"):
        with open(description_file) as f:
            try:
                ydata = yaml.safe_load(f.read())
                if isinstance(ydata, list):
                    metrics += [MetricDescription(**d) for d in ydata]
                elif isinstance(ydata, dict):
                    metrics.append(MetricDescription(**ydata))
                elif ydata is None:
                    pass
                else:
                    raise Exception("Unparsable metric description")
            except Exception as ex:
                log.error("Error when reading %s content", description_file)
                log.error("%s: %s", repr(ex), str(ex))
                log.error(traceback.format_exc())
                sys.exit(1)

    log.debug("\n  ".join((str(metric) for metric in metrics)))
    return metrics


def merge_metrics_per_device_and_protocol(metrics):
    """Merge list of metrics per involved device and returns a Dict[MetricDevice, MetricDescription]"""
    metrics_per_device = {}
    for metric in metrics:
        if metric.device not in metrics_per_device:
            metrics_per_device[metric.device] = []
        metrics_per_device[metric.device].append(metric)
    return metrics_per_device


async def schedule_every(
    period,
    func_name,
    args=[],
    kwargs={},
    delayed_start=-1,
    task_name=None,
    timeout_max_count=5,
):
    """Schedule func_name to run every period"""

    if not task_name:
        task_name = (
            f"{func_name}("
            + ", ".join(args)
            + ", "
            + ", ".join(f"{k}={v}" for k, v in kwargs.items())
        )

    if delayed_start < 0:
        delay = random.randint(0, int(period * 1000)) / 1000
    else:
        delay = delayed_start

    await asyncio.sleep(delay)

    log.debug("Start task scheduler for %s", task_name)

    while True:

        task = asyncio.create_task(func_name(*args, **kwargs))
        task.task_name = task_name + "/" + str(int(time.time()))
        log.debug("Task created: %s", task.task_name)
        timeout_count = 0

        while True:
            await asyncio.sleep(period)
            if not task.done():
                timeout_count += 1
                if timeout_count >= timeout_max_count:
                    log.error(
                        "Cancelling task that did not finished after %s periods of %s sec: %s",
                        timeout_max_count,
                        period,
                        task.task_name,
                    )
                    task.cancel()
                    break
                log.warning(
                    "Waiting for task that did not finish under its period of %s sec: %s",
                    period,
                    task.task_name,
                )
            elif task.exception():
                log.error(
                    'Task had an exception %s ["%s"], scheduling new one: %s',
                    repr(task.exception()),
                    task.exception(),
                    task.task_name,
                )
                task.print_stack()
                break
            else:
                log.debug("Task correctly finished: %s", task.task_name)
                break


async def process_host_metrics(device, metrics):
    """Process metrics query on a device"""

    log.debug(
        "Starting process_host_metrics for task: %s", asyncio.current_task().task_name
    )

    # Remove metrics having template not parsed
    metrics = [metric for metric in metrics if not metric.path_template or metric.path]

    metrics = await filter_optional_metrics(metrics)
    if not metrics:
        log.info(
            "Nothing to process after filtering optional metrics for host %s@%s",
            device.hostname,
            device.protocol,
        )
        return

    if device.protocol == "snmp":
        process_method = process_snmp_host
    elif device.protocol == "ipmisensor":
        process_method = process_ipmisensor_host
    elif device.protocol == "prometheus":
        process_method = process_prometheus_host
    else:
        log.error("Unsupported protocol for device %s", device)
        return

    # "results" stores a (timestamp, value) for each metric
    # It must have same length and ordering than fetched_metrics
    fetched_metrics, results = await process_method(device, metrics)

    if not any(results):
        log.warning(
            "Nothing to process for host %s@%s", device.hostname, device.protocol
        )
        return

    await batch_metrics_values(fetched_metrics, results)


async def process_snmp_host(device, metrics):
    """Process one query for metrics on a device using SNMP"""

    # "oids" maps SNMP OID with the associated metric position in "metrics" list
    # (the OID must be stored as string, without heading ".")
    oids = {metric.path: metric_idx for metric_idx, metric in enumerate(metrics)}

    # "results" has same length and ordering than metrics
    # (None value is used if result is not available for a metric)
    results = [None] * len(metrics)

    timestamp = time.time()
    _results = await make_snmp_request(
        device.hostname, "get", list(oids.keys()), device.username
    )
    log.debug(
        "snmpget request executed in %s for task: %s",
        time.time() - timestamp,
        asyncio.current_task().task_name,
    )

    for oid, value in _results.items():
        results[oids[oid]] = (timestamp, value)

    return metrics, results


async def process_ipmisensor_host(device, metrics):
    """Process one query for metrics on a device using IPMI"""

    command = ["/usr/sbin/ipmi-sensors"]
    command += ["--sdr-cache-recreate", "-b", "-D", "LAN_2_0", "-h", device.hostname]
    if device.username:
        command += ["-u", device.username]
    if device.password:
        command += ["-p", device.password]

    timestamp = time.time()
    process = await asyncio.get_running_loop().run_in_executor(
        ipmi_executor, functools.partial(subprocess.run, command, capture_output=True)
    )
    log.debug(
        "ipmi-sensor command executed in %s for task: %s",
        time.time() - timestamp,
        asyncio.current_task().task_name,
    )

    # "results" has same length and ordering than metrics
    # (None value is used if result is not available for a metric)
    results = [None] * len(metrics)

    if process.returncode != 0:
        log.error(
            "ipmi-sensor command %s failed for task: %s (%s)",
            command,
            asyncio.current_task().task_name,
            process.stderr,
        )
    else:
        # parse ipmi-sensor stdout and store values by sensor name and sensor ID.
        # (both ipmi-sensor's ID and name fields may be used in the MetricDescription
        # URL path but some devices use identical names for different sensor, so ID is safer)
        ipmisensor_values = {}
        for ipmisensor_output in process.stdout.decode().strip().split("\n")[1:]:
            values = [value.strip() for value in ipmisensor_output.split("|")]
            sensor_id, sensor_name, sensor_value = values[0], values[1], values[3]
            ipmisensor_values[sensor_id] = sensor_value
            ipmisensor_values[sensor_name] = sensor_value

        for metric_idx, sensor_name in enumerate(metric.path for metric in metrics):
            if sensor_name not in ipmisensor_values:
                log.warning(
                    "Could not find IPMI sensor with name or ID %s on device %s",
                    sensor_name,
                    device.hostname,
                )
            elif ipmisensor_values[sensor_name] != "N/A":
                results[metric_idx] = (timestamp, ipmisensor_values[sensor_name])

    return metrics, results


prom_re = re.compile(r"(\w+)({?.*}?) (.*)")
promlabel_re = re.compile(r"(\w+)=\"(.*?)\"")


class PrometheusMetricDescription(object):
    def __init__(self, d):
        self.__dict__ = d


async def process_prometheus_host(device, metrics):
    """Process one query for metrics on a prometheus exporter device"""

    timestamp = time.time()
    try:
        async with http_session.get(
            f"http://{device.hostname}:{device.port}/metrics"
        ) as resp:
            assert resp.status == 200
            resp_txt = await resp.text()

        log.debug(
            "Prometheus exporter returned in %s for task: %s",
            time.time() - timestamp,
            asyncio.current_task().task_name,
        )
    except aiohttp.ClientConnectorError:
        log.warning(
            "Cannot connect to Prometheus host %s:%s, skipping",
            device.hostname,
            device.port,
        )
        log.debug(traceback.format_exc())
        return [], []
    except aiohttp.ServerDisconnectedError:
        log.warning(
            "Disconnect from Prometheus host %s:%s, skipping",
            device.hostname,
            device.port,
        )
        log.debug(traceback.format_exc())
        return [], []

    fetched_metrics = []
    values = []

    allowed_metrics = None
    # If a metric do not have a path, it means it accepts all prometheus
    # metrics returned by the exporter.
    # Otherwise, the prometheus metrics to accept are those specified into pathes
    if all(metric.path for metric in metrics):
        allowed_metrics = set(
            allowed_metric
            for metric in metrics
            for allowed_metric in metric.path.split("-")
        )

    for prom_metric in resp_txt.split("\n"):

        if not (prom_metric == "" or prom_metric.startswith("#")):
            (
                prom_metric_name,
                prom_metric_label_str,
                prom_metric_value,
            ) = prom_re.match(prom_metric).groups()

            if allowed_metrics and not prom_metric_name in allowed_metrics:
                continue

            # Using a dict-based object is more efficient than a dataclass
            fetched_metric = PrometheusMetricDescription(
                {
                    "name": "prom_" + prom_metric_name,
                    "device_id": metrics[0].device_id,
                    "labels": None,
                    "scale_factor": None,
                }
            )

            if prom_metric_label_str:
                fetched_metric.labels = dict(
                    promlabel_re.findall(prom_metric_label_str)
                )

            # Parse Kwollect custom metrics pushed through exporter
            custom_timestamp = None
            if fetched_metric.name == "prom_kwollect_custom":

                fetched_metric.labels["_metric_scrape_time"] = timestamp
                fetched_metric.labels["_metric_origin"] = "prom_kwollect_custom"

                if fetched_metric.labels.get("_timestamp"):
                    try:
                        custom_timestamp = float(fetched_metric.labels["_timestamp"])
                    except (ValueError, TypeError):
                        log.warning(
                            "Cannot parse prom_kwollect_custom _timestamp label, skipping"
                        )
                        continue
                    del fetched_metric.labels["_timestamp"]

                if fetched_metric.labels.get("_metric_id"):
                    fetched_metric.name = fetched_metric.labels["_metric_id"]
                    del fetched_metric.labels["_metric_id"]

            fetched_metrics.append(fetched_metric)
            values.append((custom_timestamp or timestamp, prom_metric_value))

    log.debug(
        "Prometheus processed after %s for task: %s",
        time.time() - timestamp,
        asyncio.current_task().task_name,
    )

    return fetched_metrics, values


promoted_metrics_by_devices = {}
promoted_lastupdate = -1


async def filter_optional_metrics(metrics):
    """Query DB to filter out optional metrics from metrics argument for a device"""

    # Poor man cache to only update promoted_metrics_by_devices every seconds
    global promoted_metrics_by_devices, promoted_lastupdate
    cur_time = time.time()
    if cur_time - promoted_lastupdate > 1:
        promoted_lastupdate = cur_time
        log.debug(
            "Prepare updating promoted devices for task: %s",
            asyncio.current_task().task_name,
        )
        promoted_metrics_by_devices = {
            promoted_device: re.compile(promoted_metric)
            for promoted_device, promoted_metric in await psql_pool.fetch(
                "SELECT device_id, metric_id FROM promoted_metrics"
            )
        }
        log.debug(
            "Updated promoted metrics using SQL SELECT %d lines in %s (pool size : %d/%d) for task: %s",
            len(promoted_metrics_by_devices.keys()),
            time.time() - cur_time,
            psql_pool._queue.qsize(),
            psql_pool._maxsize,
            asyncio.current_task().task_name,
        )

    # This could be further optimized as when this function is called,
    # all metrics belong to the same device
    return [
        metric
        for metric in metrics
        if not metric.optional
        or (
            promoted_metrics_by_devices.get(metric.device_id)
            and promoted_metrics_by_devices[metric.device_id].match(metric.name)
        )
        or (
            metric.labels
            and metric.labels.get("_device_alias")
            and promoted_metrics_by_devices.get(metric.labels["_device_alias"])
            and promoted_metrics_by_devices[metric.labels["_device_alias"]].match(
                metric.nane
            )
        )
    ]


sql_values_batch = []
sql_values_lastinsert = -1


async def batch_metrics_values(metrics, results):
    """Insert metrics and associated values into DB"""

    log.debug(
        "Preparing SQL data for task: %s",
        asyncio.current_task().task_name,
    )

    sql_values = []

    for i, metric in enumerate(metrics):
        if not results[i]:
            continue
        timestamp, value = results[i]
        if value is not None:
            sql_labels = dict(metric.labels or {})
            try:
                value = float(value)
                if metric.scale_factor:
                    value = value * metric.scale_factor
            except (ValueError, TypeError):
                sql_labels.update({"value_str": value})
                value = float("NaN")
            sql_values.append(
                (
                    datetime.fromtimestamp(timestamp, tz=timezone.utc),
                    metric.device_id,
                    metric.name,
                    value,
                    json_dumps(sql_labels),
                )
            )

    global sql_values_batch
    sql_values_batch += sql_values


async def insert_metrics_values():

    global sql_values_batch, sql_values_lastinsert

    cur_time = time.time()
    if len(sql_values_batch) > 100 or cur_time - sql_values_lastinsert > 1:
        sql_values_lastinsert = cur_time
        sql_values = sql_values_batch
        sql_values_batch = []

        try:
            async with psql_pool.acquire() as con:
                cur_time = time.time()
                await con.copy_records_to_table("metrics", records=sql_values)
        except ConnectionRefusedError as ex:
            log.error("DB connection error on SQL COPY: %s", ex)
            log.debug(traceback.format_exc())
        except Exception as ex:
            log.error("Error when performing SQL COPY command, abording")
            log.error(sql_values)
            log.error(traceback.format_exc())
        log.debug(
            "Done SQL COPY %d lines in %s (pool size : %d/%d) for task: %s",
            len(sql_values),
            time.time() - cur_time,
            psql_pool._queue.qsize(),
            psql_pool._maxsize,
            asyncio.current_task().task_name,
        )
    else:
        log.debug(
            "Batching SQL data for task: %s",
            asyncio.current_task().task_name,
        )


async def parse_metrics_template(metrics_per_device):
    """Resolv metrics that use template, i.e. {{  }} in their path (only
    supported for SNMP metrics)"""

    # Parse metrics with SNMP {{ }} template in their URL
    for device, metrics in metrics_per_device.items():
        if device.protocol != "snmp":
            continue

        # Resolve templates
        if any(metric.path_template for metric in metrics):
            await parse_snmp_device_metrics_template(device, metrics)


async def parse_snmp_device_metrics_template(device, metrics):
    """Send SNMP request to retrieve OID suffixes corresponding to metrics' template
    that use {{ oidprefix == value }} in their URLs"""

    results = {}
    for metric_oidprefix in set(
        metric.parse_template()[0] for metric in metrics if metric.parse_template()
    ):
        log.debug("Getting %s values on host %s", metric_oidprefix, device.hostname)
        results[metric_oidprefix] = await make_snmp_request(
            device.hostname,
            "walk",
            metric_oidprefix,
            device.username,
            timeout=20,
            retries=2,
        )

    for metric in metrics:
        if metric.parse_template():
            template_parsed = False
            metric_oidprefix, metric_oidvalue = metric.parse_template()
            for oid, snmp_value in results.get(metric_oidprefix, {}).items():
                if snmp_value == metric_oidvalue:
                    oid_suffix = oid.replace(metric_oidprefix, "").strip(".")
                    metric.path = re.sub(r"{{.*}}", oid_suffix, metric.path_template)
                    log.debug(" resolved %s : %s", metric_oidvalue, oid_suffix)
                    template_parsed = True
            if not template_parsed:
                log.error(
                    "SNMP template %s for %s not converted, disabling metrics",
                    metric.path_template,
                    device.hostname,
                )
                metric.path = None


http_session = None


async def init_http():
    global http_session
    http_session = aiohttp.ClientSession()


psql_pool = None


async def init_psql():
    global psql_pool
    psql_pool = await asyncpg.create_pool(
        database=config["db_name"],
        user=config["db_user"],
        password=config["db_password"],
        host=config["db_host"],
    )


ipmi_executor = None


def init_ipmi():
    global ipmi_executor
    ipmi_executor = concurrent.futures.ProcessPoolExecutor(max_workers=4*config["worker"])


async def make_snmp_request(
    host, snmp_command, oids, community="public", timeout=30, retries=1
):
    """aiosnmp glue"""
    try:
        if snmp_command not in ("get", "walk"):
            raise Exception("Unsupported snmp_command (must be get or walk)")

        async with aiosnmp.Snmp(
            host=host, port=161, community=community, timeout=timeout, retries=retries
        ) as snmp:
            if snmp_command == "get":
                # Slicing OIDs to perform SNMP GET with a maximum of 50 objects and avoid fragmentation
                snmp_results = []
                for oids_slice in (
                    oids[i : min(i + 50, len(oids))] for i in (range(0, len(oids), 50))
                ):
                    log.debug("snmp.get: %s %s", host, oids_slice)
                    snmp_results += await snmp.get(oids_slice)

            if snmp_command == "walk":
                if not isinstance(oids, str):
                    raise Exception(
                        "Unsupported OID list for snmp_command walk (must be unique string)"
                    )
                log.debug("snmp.walk: %s %s", host, oids)
                snmp_results = await snmp.walk(oids)

        results = {}
        for res in snmp_results:
            results[str(res.oid).lstrip(".")] = (
                res.value.decode()
                if isinstance(res.value, (bytes, bytearray))
                else res.value
            )
        log.debug("snmp.results: %s", results)
        return results

    except asyncio.CancelledError:
        log.warning("Task cancelled when performing SNMP request, skipping...")
    except aiosnmp.exceptions.SnmpTimeoutError:
        log.error(
            "Timeout on SNMP request %s on %s %s, skipping...", snmp_command, host, oids
        )
    except Exception:
        log.error(
            "Error when performing SNMP request %s on %s with %s",
            snmp_command,
            host,
            oids,
        )
        log.error(traceback.format_exc())
    return {}


if __name__ == "__main__":
    main()
