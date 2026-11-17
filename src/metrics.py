"""Metric aggregation helpers for Helio Metrics."""

WINDOW_SECONDS = 300


def bucketise(samples, window=WINDOW_SECONDS):
    buckets = {}
    for sample in samples:
        bucket = sample.ts // window
        buckets.setdefault(bucket, []).append(sample)
    return buckets


def rolling_mean(values, span=5):
    if span <= 0:
        raise ValueError("span must be positive")
    out = []
    for index in range(len(values)):
        start = max(0, index - span + 1)
        chunk = values[start:index + 1]
        out.append(sum(chunk) / len(chunk))
    return out
