from typing import Dict, Any, List
import statistics


def correlate_metrics(args: Dict[str, Any]) -> Dict[str, Any]:
    metrics = args.get('metrics', {})
    names = list(metrics.keys())
    correlations = []
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            a = metrics[names[i]]
            b = metrics[names[j]]
            if len(a) != len(b) or len(a) == 0:
                corr = 0.0
            else:
                mean_a = statistics.mean(a)
                mean_b = statistics.mean(b)
                num = sum((x-mean_a)*(y-mean_b) for x,y in zip(a,b))
                den = (sum((x-mean_a)**2 for x in a)**0.5)*(sum((y-mean_b)**2 for y in b)**0.5)
                corr = num/den if den != 0 else 0.0
            correlations.append({"pair": (names[i], names[j]), "corr": corr})
    return {"correlations": correlations}
