from typing import Dict, Any, List
import statistics


def analyze_anomaly(args: Dict[str, Any]) -> Dict[str, Any]:
    rows = args.get('rows', [])
    values = [float(r.get('metric_value', 0)) for r in rows]
    if not values:
        return {"baseline": None, "current": None, "deviation": None, "anomaly_score": 0.0, "trend": "flat"}
    baseline = statistics.mean(values[:-1]) if len(values) > 1 else values[0]
    current = values[-1]
    deviation = current - baseline
    anomaly_score = abs(deviation) / (baseline + 1e-6)
    trend = "up" if deviation > 0 else "down" if deviation < 0 else "flat"
    return {"baseline": baseline, "current": current, "deviation": deviation, "anomaly_score": anomaly_score, "trend": trend}
