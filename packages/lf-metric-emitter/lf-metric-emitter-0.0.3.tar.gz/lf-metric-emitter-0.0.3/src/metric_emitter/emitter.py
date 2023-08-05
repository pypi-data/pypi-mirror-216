import json
import os
import requests
import time

from collections.abc import Iterable
from numbers import Number
from urllib.parse import urljoin

schema = {
    "namespace": "placholder",
    "type": "record",
    "name": "placeholder",
    "fields": [
        {
            "name": "timestamp",
            "type": "double",
        },
        {
            "name": "benchmark_env",
            "type": "string",
        },
        {
            "name": "module",
            "type": "string",
        },
        {
            "name": "benchmark_type",
            "type": "string",
        },
        {
            "name": "benchmark_unit",
            "type": "string",
        },
        {
            "name": "value",
            "type": "float",
        },
        {
            "name": "commit_hash",
            "type": "string",
        },
    ],
}

record = {
    "timestamp": 1,  # placeholder, double, seconds since epoch
    "benchmark_env": "unknown",  # One of []"github-ci", "epyc", etc.]
    "module": "placeholder",  # e.g. "ApplyColourOffset"
    "benchmark_type": "placeholder",  # One of ['runtime', 'memory', etc.]
    "benchmark_unit": "placeholder",  # One of ['s', 'Mb', 'Gb', 'count', etc.]
    "value": 1,  # placeholder
    "commit_hash": "",  # placeholder
}


class Emitter:
    def __init__(
        self,
        namespace: str = "lsst.lf",
        name: str = None,
        module: str = None,
        benchmark_type: str = None,
        benchmark_unit: str = None,
    ):
        """A simple class to emit benchmarking metrics. Almost certainly this is
        too specific, and should be abstracted with a few different child class
        implementations.

        Parameters
        ----------
        namespace : str, optional
            This is the sasquatch namespace, by default 'lsst.lf'
        name : str, optional
            This defines the fully qualified namespace, it is appended to
            `namespace`. Recommend that it be `<project_name>.bench`. For example
            `ssppIncub.bench`, or `rail.bench`. This will result in a fully
            qualified namespace like `lsst.lf.ssppIncub.bench` or
            `lsst.lf.rail.bench`. Recommend lower snake case. by default None
        module : str, optional
            The name of the module being benchmarked. For instance `applyColourOffset`.
            It is recommended to use lower snake case for this, by default None
        benchmark_type : str, optional
            The type of benchmarking. For instance: `runtime`, `memory`, etc,
            by default None
        benchmark_unit : str, optional
            The unit of the benchmark. For instance: `s`, `Mb`, `count`, etc.
            by default None
        """
        self.namespace = namespace
        self.name = name
        self.module = module
        self.benchmark_type = benchmark_type
        self.benchmark_unit = benchmark_unit
        self.record_value = None

        self.schema = schema
        self.schema["namespace"] = self.namespace
        self.schema["name"] = self.name

        self.record = record
        self.record["benchmark_env"] = os.environ.get("BENCHMARK_ENV", "unknown")
        self.record["module"] = self.module
        self.record["benchmark_type"] = self.benchmark_type
        self.record["benchmark_unit"] = self.benchmark_unit

    def set_value(self, record_value: float = None) -> None:
        """Sets a specific value to be emitted

        Parameters
        ----------
        record_value : float, optional
            Right now we assume that the values will always be floats. Clearly
            this isn't the best assumption. But for now, we assume only single
            numeric values, by default None
        """

        if isinstance(record_value, Iterable):
            raise ValueError("The `record_value` must be a single value")

        if not isinstance(record_value, Number):
            raise ValueError("The `record_value` must be numeric")

        self.record["value"] = record_value
        self.record["timestamp"] = time.time()  # double, seconds since Unix epoch

    def emit(self) -> None:
        """This actually send the recorded value to the Sasquatch stack.
        There is no error handling here, in the case of failed requests!
        """
        payload = {
            "value_schema": json.dumps(self.schema),
            "records": [{"value": self.record}],
        }

        headers = {
            "Content-Type": "application/vnd.kafka.avro.v2+json",
            "Accept": "application/vnd.kafka.v2+json",
        }

        base_url = os.environ.get("KAFKA_API_URL", None)

        if base_url is None or self.record["benchmark_env"] == "unknown":
            print(f"Base URL: {base_url}")
            print(payload)

        else:
            # results in url like: `https://example.com/lsst.example.metric.name`
            metric_name = ".".join([self.schema["namespace"], self.schema["name"]])
            full_url = urljoin(base_url, metric_name)

            response = requests.post(full_url, json=payload, headers=headers)

            if response.status_code is not 200:
                print(f"Response status code: {response.status_code}")
                print(f"Full URL: {full_url}")
                print(payload)
