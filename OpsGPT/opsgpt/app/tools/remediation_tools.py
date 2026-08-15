from typing import Dict, Any
from app.config.settings import Settings
import logging

logger = logging.getLogger(__name__)

ALLOWED_ACTIONS = {"RESTART_SERVICE", "SCALE_SERVICE", "ROLLBACK_DEPLOYMENT", "CLEAR_CACHE"}


def recommend_remediation(args: Dict[str, Any]) -> Dict[str, Any]:
    analysis = args.get('analysis', {})
    score = analysis.get('anomaly_score', 0.0)
    if score > 1.0:
        return {"action": "ROLLBACK_DEPLOYMENT", "reason": "High anomaly score after deployment", "confidence": 0.9, "risk": "MEDIUM"}
    return {"action": "RESTART_SERVICE", "reason": "Transient spike suspected", "confidence": 0.6, "risk": "LOW"}


def execute_remediation(args: Dict[str, Any]) -> Dict[str, Any]:
    settings = Settings()
    action = args.get('action')
    if action not in ALLOWED_ACTIONS:
        logger.warning("Attempted to execute unauthorized action: %s", action)
        return {"status": "REJECTED", "reason": "Unauthorized action"}

    if settings.EXECUTION_MODE != "EXECUTE":
        logger.info("Dry-run mode: would execute %s", action)
        return {"status": "DRY_RUN", "action": action}

    logger.info("Executing remediation action: %s", action)
    return {"status": "EXECUTED", "action": action}
