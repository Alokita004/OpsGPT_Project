from typing import Dict, Any
import random


def get_current_metrics(args: Dict[str, Any]) -> Dict[str, Any]:
    service = args.get('service_name')
    metric = args.get('metric_name')
    time_window = args.get('time_window', '5m')
    values = [round(random.random()*5, 2) for _ in range(6)]
    return {"service_name": service, "metric_name": metric, "time_window": time_window, "values": values}
