from typing import Dict, Any


def generate_diagnosis(args: Dict[str, Any]) -> Dict[str, Any]:
    analysis = args.get('analysis', {})
    deployments = args.get('deployments', [])
    anomaly_score = analysis.get('anomaly_score', 0.0)
    root = "unknown"
    summary = "No clear root cause determined"

    if deployments:
        # Prefer latest deployment as potential root cause
        latest = deployments[-1]
        ver = latest.get('version') or latest.get('revision') or 'unknown'
        root = f"deployment_{ver}"
        summary = f"Potential deployment-related regression in {ver}"

    return {"summary": summary, "root_cause": root, "confidence": anomaly_score, "explanation": "Auto-generated diagnosis"}
