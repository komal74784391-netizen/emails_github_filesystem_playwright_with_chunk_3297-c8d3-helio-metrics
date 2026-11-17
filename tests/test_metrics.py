from src.metrics import bucketise, rolling_mean
from src.collector import Sample


def test_rolling_mean_window():
    assert rolling_mean([1.0, 2.0, 3.0], span=2) == [1.0, 1.5, 2.5]


def test_bucketise_groups_by_window():
    samples = [Sample(0, "cpu", 0.5, {}), Sample(1, "cpu", 0.7, {})]
    assert len(bucketise(samples, window=1)) == 2
