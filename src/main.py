import csv
from models.eligibility_scoring import calculate_eligibility_score
from models.recommendation_advisor import generate_recommendation_report

user_profile = {
    "name": "Ravi",
    "income": 180000,
    "state": "Telangana",
    "category": "Student"
}

eligibility_results = []

with open("src/data/schemes_master.csv", newline="") as file:
    reader = csv.DictReader(file)
    schemes = list(reader)

print("\n🔍 AI Eligibility & Risk Analysis Report\n")

for scheme in schemes:
    scheme["min_income"] = int(scheme["min_income"])
    scheme["max_income"] = int(scheme["max_income"])
    scheme["estimated_benefit"] = int(scheme["estimated_benefit"])

    result = calculate_eligibility_score(user_profile, scheme)

    result["scheme"] = scheme["scheme_name"]
    result["scheme_data"] = scheme

    eligibility_results.append(result)

for result in eligibility_results:
    report = generate_recommendation_report(result)

    print(f"🏷️ Scheme: {report['scheme']}")
    print(f"📊 Score: {report['score']} | Confidence: {report['confidence']}")
    print(f"🚦 Priority: {report['priority']}")
    print(f"⏱️ Urgency: {report['urgency']} | Risk: {report['risk_level']}")
    print(f"{report['warning']}")
    print(f"💸 {report['estimated_loss']}")

    print("Reasons:")
    for r in report["reasons"]:
        print(f" - {r}")

    print("Required Documents:")
    for d in report["required_documents"]:
        print(f" - {d}")

    print("-" * 60)
