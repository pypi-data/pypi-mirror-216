# lf-metric-emitter
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/lincc-frameworks/metric-emitter)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/lincc-frameworks/metric-emitter/testing-and-coverage.yml)

This tool encapsulates the code needed to emit metrics to the Sasquatch InfluxDB
stack. https://sasquatch.lsst.io/index.html

To utilize this tool, two environment variables must be set:
1) `BENCHMARK_ENV` should be set to something consistent, for instance, `github-ci`, `epic`, `local-desktop-1`, etc.
2) `KAFKA_API_URL` should be set to the full url. See the Sasquatch documentation for the specific URL.

You'll also need to manually create a Kafka topic to receive the metrics that are
emitted. Again, see the Sasquatch documentation for instructions.

With the Kafka topic created, and the environmental variables, metrics can be emitted like so:

```
# result from a timing bench mark
my_result = 42.0

emitter = Emitter(namespace='lsst.lf',
                 name='ssppIncubator.bench',
                 module='PPApplyColourOffset',
                 benchmark_type:'runtime',
                 benchmark_unit:'s')


emitter.set_value(my_result)
emitter.emit()
```

[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)

This project was automatically generated using the LINCC-Frameworks [python-project-template](https://github.com/lincc-frameworks/python-project-template).

For more information about the project template see the For more information about the project template see the [documentation](https://lincc-ppt.readthedocs.io/en/latest/).
