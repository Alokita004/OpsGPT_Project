from app.tools.registry import registry, Tool
from app.tools.bigquery_tools import query_historical_metrics
from app.tools.analysis_tools import analyze_anomaly
from app.tools.remediation_tools import recommend_remediation, execute_remediation
from app.tools.correlate_tools import correlate_metrics
from app.tools.current_metrics import get_current_metrics
from app.tools.deployments_tools import get_recent_deployments
from app.tools.diagnosis_tools import generate_diagnosis


def setup_tools():
    registry.register(Tool(name="query_historical_metrics", description="Query historical metrics", func=query_historical_metrics))
    registry.register(Tool(name="analyze_anomaly", description="Analyze anomaly", func=analyze_anomaly))
    registry.register(Tool(name="recommend_remediation", description="Recommend remediation", func=recommend_remediation))
    registry.register(Tool(name="execute_remediation", description="Execute remediation", func=execute_remediation))
    registry.register(Tool(name="correlate_metrics", description="Correlate metrics", func=correlate_metrics))
    registry.register(Tool(name="get_current_metrics", description="Get current metrics", func=get_current_metrics))
    registry.register(Tool(name="get_recent_deployments", description="Get recent deployments", func=get_recent_deployments))
    registry.register(Tool(name="generate_diagnosis", description="Generate diagnosis", func=generate_diagnosis))


setup_tools()
