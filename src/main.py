import csv
from models.eligibility_scoring import calculate_eligibility_score
from models.recommendation_advisor import generate_recommendation_report
from models.scenario_engine import simulate_income_scenarios
from models.ranking_engine import rank_schemes


user_profile = {
    "name": "Ravi",
    "income": 180000,
    "state": "Telangana",
    "category": "Student"
}

eligibility_results = []
enriched_reports = []   # ✅ REQUIRED for ranking

with open("src/data/schemes_master.csv", newline="") as file:
    reader = csv.DictReader(file)
    schemes = list(reader)

print("\n🔍 AI Eligibility & Risk Analysis Report\n")

# -------- Eligibility + Advisory --------
for scheme in schemes:
    scheme["min_income"] = int(scheme["min_income"])
    scheme["max_income"] = int(scheme["max_income"])
    scheme["estimated_benefit"] = int(scheme["estimated_benefit"])
    scheme["priority_weight"] = int(scheme["priority_weight"])

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

    # 🔥 Prepare data for ranking engine
    enriched_reports.append({
        "scheme": report["scheme"],
        "score": report["score"],
        "priority_weight": result["scheme_data"]["priority_weight"],
        "deadline": result["scheme_data"]["deadline"],
        "estimated_benefit": result["scheme_data"]["estimated_benefit"]
    })

# -------- WHAT-IF SIMULATION --------
print("\n🧪 WHAT-IF INCOME SIMULATION\n")

income_tests = [
    user_profile["income"] - 50000,
    user_profile["income"],
    user_profile["income"] + 50000
]

for scheme in schemes:
    print(f"Scheme: {scheme['scheme_name']}")
    simulations = simulate_income_scenarios(
        user_profile, scheme, income_tests
    )

    for s in simulations:
        status = "ELIGIBLE" if s["eligible"] else "NOT ELIGIBLE"
        print(f"  Income ₹{s['income']} → {status}")

    print("-" * 40)

# -------- FINAL RANKING --------
print("\n🏆 AI FINAL APPLICATION PRIORITY RANKING\n")

ranked = rank_schemes(enriched_reports)

for idx, r in enumerate(ranked, 1):
    print(f"{idx}. {r['scheme']} (Rank Score: {r['rank_score']})")
