#!/usr/bin/python3

import requests
import pytest
import time
import json
import datetime


def metrics(params):
    r = requests.get("http://localhost:3000/rpc/get_metrics", params=params)
    assert r.ok
    return r.json()


def metrics_available(params={}):
    r = requests.post(
        "http://localhost:3000/rpc/available_metrics",
        data=json.dumps(params),
        headers={"Content-Type": "application/json"},
    )
    assert r.ok
    return r.json()


def test_metrics():
    assert len(metrics({"devices": "local"})) > 0


def test_metrics_start():
    r = metrics({"devices": "device-1", "start_time": "2020-12-31T23:00:00"})
    assert len(r) > 0
    assert all("2020-12-31T23:0" in m["timestamp"] for m in r)
    assert all("device-1" == m["device_id"] for m in r)


def test_metrics_end():
    r = metrics({"devices": "device-1", "end_time": "2020-12-31T23:19:59"})
    assert len(r) > 0
    assert all("2020-12-31T23:1" in m["timestamp"] for m in r)


def test_metrics_startend():
    r = metrics(
        {
            "devices": "device-1",
            "start_time": "2020-12-31T23:00:00",
            "end_time": "2020-12-31T23:00:59",
        }
    )
    assert len(r) > 0
    assert all("2020-12-31T23:00" in m["timestamp"] for m in r)


def test_metrics_devices():
    assert 2 * len(
        metrics({"devices": "device-1", "start_time": "2020-12-31T22:59:59"})
    ) == pytest.approx(
        len(
            metrics(
                {"devices": "device-1,device-2", "start_time": "2020-12-31T22:59:59"}
            )
        )
    )


def test_metrics_metric():
    assert all(
        r["metric_id"] == "metric-1"
        for r in metrics(
            {
                "devices": "device-1",
                "start_time": "2020-12-31T22:59:59",
                "metrics": "metric-1",
            }
        )
    )


def test_metrics_job():
    r = metrics({"job_id": 1})
    assert all(m["device_id"] in ("device-1", "device-2") for m in r)
    assert r[0]["timestamp"] == "2020-12-31T22:00:00+00:00"
    assert r[-1]["timestamp"] == "2020-12-31T23:00:00+00:00"


def test_metrics_job_devices():
    assert all(
        r["device_id"] == "device-1"
        for r in metrics({"job_id": 1, "devices": "device-1"})
    )


def test_job_metric():
    assert all(
        r["metric_id"] == "metric-1"
        for r in metrics(
            {
                "job_id": 1,
                "metrics": "metric-1",
            }
        )
    )


def test_metrics_job_start():
    assert (
        metrics({"job_id": 1, "start_time": "2020-12-31T22:29:59.999"})[0]["timestamp"]
        == "2020-12-31T22:30:00+00:00"
    )


def test_metrics_job_end():
    assert (
        metrics(
            {
                "job_id": 1,
                "start_time": "2020-12-31T22:29:59.999",
                "end_time": "2020-12-31T22:40:00.0001",
            }
        )[0]["timestamp"]
        == "2020-12-31T22:30:00+00:00"
    )
    assert (
        metrics(
            {
                "job_id": 1,
                "start_time": "2020-12-31T22:29:59.999",
                "end_time": "2020-12-31T22:40:00.0001",
            }
        )[-1]["timestamp"]
        == "2020-12-31T22:40:00+00:00"
    )


def test_metrics_job_notfinished():
    r = metrics({"job_id": 3})
    assert any(str(datetime.date.today()) in m["timestamp"] for m in r)
    r = metrics({"job_id": 3, "end_time": "2020-12-31T23:59:59"})
    assert not any(str(datetime.date.today()) in m["timestamp"] for m in r)


def test_available_metrics():
    # devices from last min
    assert len(metrics_available()) > -1


def test_available_metrics_old():
    # devices from last 5 min
    assert not any(
        m["device_id"] == "local"
        for m in metrics_available({"at": "2020-12-31T22:59:59"})
    )


def test_available_metrics_devices():
    # devices from last 5 min
    assert len(metrics_available({"params": {"devices": ["notexist"]}})) == 0


def test_available_metrics_both():
    # devices from last 5 min
    assert all(
        m["device_id"] in ("device-1", "device-2")
        for m in metrics_available(
            {
                "at": "2020-12-31T22:59:59",
                "params": {"devices": ["device-1", "device-2"]},
            }
        )
    )


def test_available_metrics_job():
    # terminated job
    assert all(
        m["device_id"] in ("device-1", "device-2")
        for m in metrics_available({"params": {"job_id": 1}})
    )


def test_available_metrics_jobrun():
    # running job
    assert all(
        m["device_id"] == "local" for m in metrics_available({"params": {"job_id": 3}})
    )


def test_kwollect_snmp():
    assert (
        len(
            metrics(
                {
                    "devices": "local",
                    "metrics": "snmp_dumb",
                }
            )
        )
        > 0
    )


def test_kwollect_snmptemplate():
    assert (
        len(
            metrics(
                {
                    "devices": "local",
                    "metrics": "snmp_template",
                }
            )
        )
        > 0
    )


def test_kwollect_prom():
    assert (
        len(
            metrics(
                {
                    "devices": "local",
                    "metrics": "prom_node_load1",
                }
            )
        )
        > 0
    )
