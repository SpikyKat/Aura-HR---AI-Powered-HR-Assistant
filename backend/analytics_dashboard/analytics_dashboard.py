import json
import os
from collections import defaultdict
import pandas as pd

ANALYTICS_FILE = "analytics_data.json"

def log_data(log_type, data):
    """
    Logs a new data point to the analytics file.
    """
    if not os.path.exists(ANALYTICS_FILE):
        analytics_data = {"fit_scores": [], "jds_generated": 0, "policy_questions": []}
    else:
        with open(ANALYTICS_FILE, 'r') as f:
            try:
                analytics_data = json.load(f)
            except json.JSONDecodeError:
                analytics_data = {"fit_scores": [], "jds_generated": 0, "policy_questions": []}

    if log_type == "fit_score":
        analytics_data["fit_scores"].append(data)
    elif log_type == "jd_generated":
        analytics_data["jds_generated"] = analytics_data.get("jds_generated", 0) + 1
    elif log_type == "policy_question":
        analytics_data["policy_questions"].append(data)

    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(analytics_data, f, indent=4)

def get_analytics_data():
    """
    Reads and processes the analytics data for visualization.
    """
    if not os.path.exists(ANALYTICS_FILE):
        return {
            "total_screenings": 0,
            "total_jds_generated": 0,
            "avg_fit_score": 0,
            "avg_score_by_role": {},
            "common_policy_questions": []
        }

    with open(ANALYTICS_FILE, 'r') as f:
        try:
            analytics_data = json.load(f)
        except json.JSONDecodeError:
            return {} # Return empty if file is corrupt

    # Calculate total screenings and average fit score
    fit_scores = analytics_data.get("fit_scores", [])
    total_screenings = len(fit_scores)
    avg_fit_score = sum(item['score'] for item in fit_scores) / total_screenings if total_screenings > 0 else 0

    # Calculate average fit score by role
    scores_by_role = defaultdict(lambda: {'total_score': 0, 'count': 0})
    for item in fit_scores:
        role = item.get('role', 'Unknown Role')
        scores_by_role[role]['total_score'] += item['score']
        scores_by_role[role]['count'] += 1

    avg_score_by_role = {
        role: data['total_score'] / data['count']
        for role, data in scores_by_role.items()
    }

    # Get common policy questions
    policy_questions = analytics_data.get("policy_questions", [])
    question_counts = pd.Series(policy_questions).value_counts().nlargest(5)


    return {
        "total_screenings": total_screenings,
        "total_jds_generated": analytics_data.get("jds_generated", 0),
        "avg_fit_score": round(avg_fit_score, 2),
        "avg_score_by_role": avg_score_by_role,
        "common_policy_questions": question_counts.to_dict()
    }
