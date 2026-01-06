import csv
from models.eligibility_scoring import calculate_eligibility_score
from models.recommendation_advisor import generate_recommendation_report

user_profile = {
    "name": "Ravi",
    "income": 180000,
    "state": "Telangana",
    "category": "Student"
}

eligibility_results = []   # ✅ REQUIRED

with open("src/data/schemes_master.csv", newline="") as file:
    reader = csv.DictReader(file)
    schemes = list(reader)

print("Eligibility Results:\n")

for scheme in schemes:
    scheme["min_income"] = int(scheme["min_income"])
    scheme["max_income"] = int(scheme["max_income"])

    result = calculate_eligibility_score(user_profile, scheme)

    # 🔥 MOST IMPORTANT LINE (FIX)
    result["scheme"] = scheme["scheme_name"]

    eligibility_results.append(result)

    print(f"Scheme: {scheme['scheme_name']}")
    print(f"Score: {result['score']}")
    print(f"Confidence: {result['confidence']}")
    print("Reasons:")
    for r in result["reasons"]:
        print(f" - {r}")
    print("-" * 50)

print("\nAI Recommendation Advisory Reports:\n")

for result in eligibility_results:
    report = generate_recommendation_report(result)

    print(f"Scheme: {report['scheme']}")
    print(f"Priority: {report['priority']}")
    print(f"Score: {report['score']} | Confidence: {report['confidence']}")

    print("Reasons:")
    for r in report["reasons"]:
        print(f" - {r}")

    print("Required Documents:")
    for d in report["required_documents"]:
        print(f" - {d}")

    print("Next Steps:")
    for step in report["next_steps"]:
        print(f" - {step}")

    print("-" * 50)
