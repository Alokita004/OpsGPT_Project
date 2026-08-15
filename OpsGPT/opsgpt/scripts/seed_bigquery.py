"""Seed CSV data used by LocalBigQueryClient for local development and tests."""
import csv
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

FILE = os.path.join(DATA_DIR, "service_metrics.csv")

def generate_rows():
    services = ["checkout-service", "payment-service", "inventory-service", "user-service"]
    metrics = ["error_rate", "latency_ms", "cpu_usage", "memory_usage", "request_count"]
    base_time = datetime.utcnow()
    rows = []
    for s in services:
        for i in range(10):
            t = base_time - timedelta(minutes=i*5)
            rows.append({
                "timestamp": t.isoformat(),
                "service_name": s,
                "environment": "PRODUCTION",
                "metric_name": metrics[i % len(metrics)],
                "metric_value": float(i * 1.5),
                "region": "us-central1",
                "version": "v1.0.%d" % i,
            })
    return rows


def seed():
    rows = generate_rows()
    with open(FILE, "w", newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=["timestamp", "service_name", "environment", "metric_name", "metric_value", "region", "version"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("Wrote", len(rows), "rows to", FILE)


if __name__ == "__main__":
    seed()
