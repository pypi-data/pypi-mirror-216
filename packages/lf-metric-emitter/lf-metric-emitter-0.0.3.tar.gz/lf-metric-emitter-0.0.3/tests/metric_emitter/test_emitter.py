from metric_emitter.emitter import Emitter


def test_emitter():
    e = Emitter(namespace="lsst.lf", name="test.fake_metric", benchmark_type="run", benchmark_unit="s")

    test_value = 42.0
    e.set_value(test_value)

    assert e.record["value"] == test_value
