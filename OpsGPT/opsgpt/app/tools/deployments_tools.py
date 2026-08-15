from typing import Dict, Any, List
import datetime


def get_recent_deployments(args: Dict[str, Any]) -> Dict[str, Any]:
    service = args.get('service_name')
    now = datetime.datetime.utcnow()
    deployments = [{"id": "d1", "time": (now - datetime.timedelta(minutes=15)).isoformat(), "revision": "rev-123"}]
    return {"service_name": service, "deployments": deployments}
